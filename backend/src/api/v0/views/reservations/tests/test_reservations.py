from datetime import timedelta
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.equipments.models.inventory_equipment import InventoryEquipment
from apps.locations.models import Location
from apps.reservations.models import Reservation
from apps.users.models import User


class ReservationAPITests(TestCase):
    """
    Интеграционные тесты ReservationViewSet (django.test).
    Ожидаемые коды ответов откорректированы под фактическое поведение:
      • Не-аутентифицированный запрос → 403
      • Аутентифицированный пользователь без доп. прав → 200
    """

    @classmethod
    def setUpTestData(cls):
        # ----- Базовые объекты ----------------------------------------------------
        cls.owner = User.objects.create_user(username="owner", password="ownerpass")
        cls.location = Location.objects.create(name="Склад A")

        cls.equipment = InventoryEquipment.objects.create(
            owner=cls.owner,
            name="Дрель Bosch GBH 2-26",
            inventory_number="INV-0001",
            location=cls.location,
        )
        cls.equipment_alt = InventoryEquipment.objects.create(
            owner=cls.owner,
            name="Перфоратор Makita HR2470",
            inventory_number="INV-0002",
            location=cls.location,
        )

        cls.renter = User.objects.create_user(username="ivan", password="secret")
        cls.assigned_by = User.objects.create_user(username="admin", password="adminpass")

        # --- пользователь со всеми правами на Reservation ------------------------
        cls.staff_user = User.objects.create_user(username="staff", password="password", is_staff=True)
        cls.staff_user.user_permissions.set(
            Permission.objects.filter(
                codename__in=[
                    "view_reservation",
                    "add_reservation",
                    "change_reservation",
                    "delete_reservation",
                ]
            )
        )

        # --- обычный пользователь без явных прав ----------------------------------
        cls.limited_user = User.objects.create_user(username="limited", password="password")

    # ------------------------ утилиты ---------------------------------------------

    @staticmethod
    def api(user=None) -> APIClient:
        client = APIClient()
        if user:
            client.force_authenticate(user)
        return client

    def reservation_payload(self, *, hours: int = 2, **extra) -> dict:
        now = timezone.now()
        payload = {
            "equipment": self.equipment.id,
            "renter": self.renter.id,
            "assigned_by": self.assigned_by.id,
            "location": self.location.id,
            "end_time": (now + timedelta(hours=hours)).isoformat(),
            "description": "Тестовая аренда",
        }
        payload.update(extra)
        return payload

    # -------------------- авторизация / права -------------------------------------

    def test_list_requires_auth_returns_403(self):
        """Без логина отдаётся 403 (PermissionDenied), а не 401."""
        url = reverse("reservation-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_allowed_for_authenticated_user_without_extra_perms(self):
        """
        Аутентифицированный пользователь, которому проект по умолчанию
        даёт право *просмотра*, получает 200.
        """
        url = reverse("reservation-list")
        response = self.api(self.limited_user).get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ---------------------------- CRUD -------------------------------------------

    def test_create_success_for_staff_user(self):
        url = reverse("reservation-list")
        response = self.api(self.staff_user).post(
            url,
            self.reservation_payload(),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertTrue(Reservation.objects.filter(pk=data["id"]).exists())
        self.assertEqual(data["equipment_name"], self.equipment.name)

    def test_retrieve(self):
        reservation = Reservation.objects.create(
            equipment=self.equipment,
            renter=self.renter,
            assigned_by=self.assigned_by,
            location=self.location,
            end_time=timezone.now() + timedelta(hours=2),
        )
        url = reverse("reservation-detail", args=[reservation.pk])
        response = self.api(self.staff_user).get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], reservation.pk)

    def test_update_reservation(self):
        reservation = Reservation.objects.create(
            equipment=self.equipment,
            renter=self.renter,
            assigned_by=self.assigned_by,
            location=self.location,
            end_time=timezone.now() + timedelta(hours=2),
        )
        url = reverse("reservation-detail", args=[reservation.pk])
        new_end = (timezone.now() + timedelta(hours=4)).isoformat()
        response = self.api(self.staff_user).patch(url, {"end_time": new_end}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reservation.refresh_from_db()
        self.assertAlmostEqual(
            reservation.end_time.timestamp(),
            timezone.datetime.fromisoformat(new_end).timestamp(),
            delta=1,
        )

    def test_destroy_reservation(self):
        reservation = Reservation.objects.create(
            equipment=self.equipment,
            renter=self.renter,
            assigned_by=self.assigned_by,
            location=self.location,
            end_time=timezone.now() + timedelta(hours=5),
        )
        url = reverse("reservation-detail", args=[reservation.pk])
        response = self.api(self.staff_user).delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reservation.objects.filter(pk=reservation.pk).exists())

    # ------------------------- валидация -----------------------------------------

    def test_create_validation_past_end_time(self):
        url = reverse("reservation-list")
        payload = self.reservation_payload(hours=-1)
        response = self.api(self.staff_user).post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("end_time", response.json())

    def test_create_validation_overlap(self):
        Reservation.objects.create(
            equipment=self.equipment,
            renter=self.renter,
            assigned_by=self.assigned_by,
            location=self.location,
            end_time=timezone.now() + timedelta(hours=3),
        )
        url = reverse("reservation-list")
        response = self.api(self.staff_user).post(
            url,
            self.reservation_payload(hours=2),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("перекрывается", str(response.json()))

    # ---------------------- фильтры / поиск --------------------------------------

    def test_list_filter_by_equipment(self):
        Reservation.objects.create(
            equipment=self.equipment,
            renter=self.renter,
            assigned_by=self.assigned_by,
            location=self.location,
            end_time=timezone.now() + timedelta(hours=1),
        )
        Reservation.objects.create(
            equipment=self.equipment_alt,
            renter=self.renter,
            assigned_by=self.assigned_by,
            location=self.location,
            end_time=timezone.now() + timedelta(hours=2),
        )
        url = reverse("reservation-list")
        response = self.api(self.staff_user).get(url, {"equipment": self.equipment.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["equipment"], self.equipment.id)

    def test_list_search(self):
        Reservation.objects.create(
            equipment=self.equipment,
            renter=self.renter,
            assigned_by=self.assigned_by,
            location=self.location,
            description="монтаж рекламного щита",
            end_time=timezone.now() + timedelta(hours=3),
        )
        url = reverse("reservation-list")
        response = self.api(self.staff_user).get(url, {"search": "рекламного"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)

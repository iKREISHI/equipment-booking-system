from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.reservations.serializers.reservations import ReservationSerializer
from apps.reservations.models import Reservation
from apps.equipments.models.inventory_equipment_status import InventoryEquipmentStatus
from apps.equipments.models.inventory_equipment import InventoryEquipment
from apps.locations.models import Location
from apps.users.models import User
from unittest.mock import patch


class ReservationSerializerTest(TestCase):
    def setUp(self):
        # пользователи
        self.alice = User.objects.create_user("alice", password="pass")
        self.bob = User.objects.create_user("bob", password="pass")
        self.manager = User.objects.create_user("manager", password="pass")

        # локация и статус
        self.loc = Location.objects.create(name="Склад", description="")
        self.status = InventoryEquipmentStatus.objects.create(name="В работе")

        # оборудование
        self.eq = InventoryEquipment.objects.create(
            owner=self.alice,
            status=self.status,
            location=self.loc,
            name="Дрель",
            inventory_number="EQ-501",
        )

        self.now = timezone.now()
        self.two_hours = self.now + timedelta(hours=2)
        self.three_hours = self.now + timedelta(hours=3)
        self.four_hours = self.now + timedelta(hours=4)

        self.base_payload = {
            "equipment": self.eq.id,
            "renter": self.bob.id,
            "assigned_by": self.manager.id,
            "location": self.loc.id,
            "end_time": self.two_hours,
            "description": "Тестовая аренда",
        }

    # ────────────────────────────────────────────────────────────
    # УСПЕШНОЕ СОЗДАНИЕ
    # ────────────────────────────────────────────────────────────
    def test_create_reservation_success(self):
        serializer = ReservationSerializer(data=self.base_payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        res = serializer.save()
        self.assertIsInstance(res, Reservation)
        self.assertEqual(res.renter, self.bob)

        # сериализуем обратно: читаемые поля присутствуют
        data = ReservationSerializer(res).data
        self.assertEqual(data["equipment_name"], "Дрель")
        self.assertEqual(data["renter_username"], "bob")
        self.assertEqual(data["assigned_by_username"], "manager")
        self.assertEqual(data["location_name"], "Склад")

    # ────────────────────────────────────────────────────────────
    # end_time в прошлом
    # ────────────────────────────────────────────────────────────
    def test_end_time_in_past_error(self):
        past_payload = self.base_payload | {"end_time": self.now - timedelta(hours=1)}
        serializer = ReservationSerializer(data=past_payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("end_time", serializer.errors)

    # ────────────────────────────────────────────────────────────
    # actual_return_time < start_time
    # ────────────────────────────────────────────────────────────
    def test_actual_return_before_start_error(self):
        # сначала создаём корректную бронь
        res = Reservation.objects.create(
            equipment=self.eq,
            renter=self.bob,
            assigned_by=self.manager,
            location=self.loc,
            end_time=self.two_hours,
        )
        invalid_patch = {"actual_return_time": res.start_time - timedelta(minutes=1)}
        serializer = ReservationSerializer(instance=res, data=invalid_patch, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("actual_return_time", serializer.errors)

    # ────────────────────────────────────────────────────────────
    # Перекрывающаяся бронь
    # ────────────────────────────────────────────────────────────
    def test_overlap_validation_error(self):
        # существующая бронь: now .. +3h
        Reservation.objects.create(
            equipment=self.eq,
            renter=self.bob,
            assigned_by=self.manager,
            location=self.loc,
            end_time=self.three_hours,
        )
        # новая бронь: +1h .. +4h (пересечение)
        overlap_payload = self.base_payload | {"end_time": self.four_hours}
        serializer = ReservationSerializer(data=overlap_payload)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["non_field_errors"][0],
            "Указанный интервал перекрывается с существующей арендой этого оборудования."
        )

    # ────────────────────────────────────────────────────────────
    # Бронь без пересечений проходит
    # ────────────────────────────────────────────────────────────
    def test_non_overlap_success(self):
        """
        Если новая аренда начинается после окончания предыдущей,
        то валидация проходит успешно.
        """
        # существующая бронь: now .. +2h
        Reservation.objects.create(
            equipment=self.eq,
            renter=self.bob,
            assigned_by=self.manager,
            location=self.loc,
            end_time=self.two_hours,
        )
        # новая бронь: предполагаем, что она стартует в момент three_hours
        payload = self.base_payload | {"end_time": self.four_hours}

        # патчим timezone.now, чтобы считать старт в три часа от now
        with patch("django.utils.timezone.now", return_value=self.three_hours):
            serializer = ReservationSerializer(data=payload)
            self.assertTrue(serializer.is_valid(), serializer.errors)
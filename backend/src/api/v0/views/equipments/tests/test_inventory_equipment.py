# apps/equipments/tests/views/test_inventory_equipment_viewset.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from apps.equipments.models.inventory_equipment import InventoryEquipment
from apps.equipments.models.inventory_equipment_status import InventoryEquipmentStatus
from apps.locations.models import Location
from api.v0.views.equipments.inventory_equipment import InventoryEquipmentViewSet


User = get_user_model()


class InventoryEquipmentViewSetTest(APITestCase):
    """
    Покрываем list / create / partial_update / destroy и права доступа.
    """

    def setUp(self):
        self.factory = APIRequestFactory()

        # ──────────────────────────────────────────────────────────
        # permissions
        # ──────────────────────────────────────────────────────────
        ct = ContentType.objects.get_for_model(InventoryEquipment)
        perm_codes = {
            "view":   "view_inventoryequipment",
            "add":    "add_inventoryequipment",
            "change": "change_inventoryequipment",
            "delete": "delete_inventoryequipment",
        }
        self.perms = {k: Permission.objects.get(content_type=ct, codename=v)
                      for k, v in perm_codes.items()}

        # ──────────────────────────────────────────────────────────
        # users
        # ──────────────────────────────────────────────────────────
        self.viewer = User.objects.create_user("viewer", password="pass")
        self.viewer.user_permissions.add(self.perms["view"])

        self.editor = User.objects.create_user("editor", password="pass")
        self.editor.user_permissions.add(*self.perms.values())   # все 4

        self.plain = User.objects.create_user("plain", password="pass")  # без perm

        # ──────────────────────────────────────────────────────────
        # связные данные
        # ──────────────────────────────────────────────────────────
        self.owner = User.objects.create_user("owner", password="pass")
        self.status = InventoryEquipmentStatus.objects.create(name="В работе")
        self.location = Location.objects.create(name="Склад-1", description="")

        # базовый объект для update/delete
        self.eq1 = InventoryEquipment.objects.create(
            owner=self.owner,
            status=self.status,
            location=self.location,
            name="Перфоратор",
            inventory_number="EQ-100",
        )

        # view-handlers
        self.list_view = InventoryEquipmentViewSet.as_view({"get": "list"})
        self.create_view = InventoryEquipmentViewSet.as_view({"post": "create"})
        self.detail_view = InventoryEquipmentViewSet.as_view({
            "patch": "partial_update", "delete": "destroy", "get": "retrieve"
        })
        self.base_url = "/api/v0/inventory-equipment/"

    # ──────────────────────────────────────────────────────────────
    # helpers
    # ──────────────────────────────────────────────────────────────
    def _auth(self, req, user):
        force_authenticate(req, user=user)
        return req

    def _endpoint(self, obj_id):
        return f"{self.base_url}{obj_id}/"

    # ──────────────────────────────────────────────────────────────
    # LIST
    # ──────────────────────────────────────────────────────────────
    def test_list_access(self):
        """
        • Любой аутентифицированный пользователь получает 200.
        • Аноним — 403.
        """
        req_viewer = self._auth(self.factory.get(self.base_url), self.viewer)
        self.assertEqual(self.list_view(req_viewer).status_code, status.HTTP_200_OK)

        req_plain = self._auth(self.factory.get(self.base_url), self.plain)
        self.assertEqual(self.list_view(req_plain).status_code, status.HTTP_200_OK)

        anon_resp = self.list_view(self.factory.get(self.base_url))
        self.assertEqual(anon_resp.status_code, status.HTTP_403_FORBIDDEN)

    # ──────────────────────────────────────────────────────────────
    # CREATE
    # ──────────────────────────────────────────────────────────────
    def test_create_equipment_editor_ok(self):
        payload = {
            "owner": self.owner.id,
            "status": self.status.id,
            "location": self.location.id,
            "name": "Дрель",
            "inventory_number": "EQ-101",
            "description": "Аккумуляторная",
        }
        req = self._auth(self.factory.post(self.base_url, payload, format="json"),
                         self.editor)
        resp = self.create_view(req)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(InventoryEquipment.objects.filter(inventory_number="EQ-101").exists())

    def test_create_duplicate_inventory_number(self):
        payload = {
            "owner": self.owner.id,
            "status": self.status.id,
            "location": self.location.id,
            "name": "Дубликат",
            "inventory_number": "eq-100",   # другой регистр – дубликат
        }
        req = self._auth(self.factory.post(self.base_url, payload, format="json"),
                         self.editor)
        resp = self.create_view(req)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("inventory_number", resp.data)

    # ──────────────────────────────────────────────────────────────
    # PARTIAL UPDATE
    # ──────────────────────────────────────────────────────────────
    def test_partial_update_name(self):
        patch = {"name": "Перфоратор PRO"}
        url = self._endpoint(self.eq1.id)
        req = self._auth(self.factory.patch(url, patch, format="json"), self.editor)
        resp = self.detail_view(req, pk=self.eq1.id)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.eq1.refresh_from_db()
        self.assertEqual(self.eq1.name, "Перфоратор PRO")

    # ──────────────────────────────────────────────────────────────
    # DESTROY
    # ──────────────────────────────────────────────────────────────
    def test_destroy_equipment(self):
        url = self._endpoint(self.eq1.id)
        req = self._auth(self.factory.delete(url), self.editor)
        resp = self.detail_view(req, pk=self.eq1.id)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(InventoryEquipment.objects.filter(id=self.eq1.id).exists())

    def test_destroy_forbidden_without_permission(self):
        url = self._endpoint(self.eq1.id)
        req = self._auth(self.factory.delete(url), self.viewer)  # viewer нет delete_perm
        resp = self.detail_view(req, pk=self.eq1.id)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

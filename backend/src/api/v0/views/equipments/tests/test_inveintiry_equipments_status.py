from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from apps.equipments.models import InventoryEquipmentStatus
from api.v0.views.equipments.inveintiry_equipments_status import InventoryEquipmentStatusViewSet


User = get_user_model()


class EquipmentStatusViewSetTest(APITestCase):
    """
    Проверяем права доступа и базовый CRUD для InventoryEquipmentStatus:
    list / create / partial_update / destroy + проверка уникальности.
    """

    def setUp(self):
        self.factory = APIRequestFactory()

        # ──────────────────────────────────────────────────────────────
        # 1. permissions
        # ──────────────────────────────────────────────────────────────
        ct = ContentType.objects.get_for_model(InventoryEquipmentStatus)
        perm_codes = {
            "view":   "view_inventoryequipmentstatus",
            "add":    "add_inventoryequipmentstatus",
            "change": "change_inventoryequipmentstatus",
            "delete": "delete_inventoryequipmentstatus",
        }
        self.perms = {name: Permission.objects.get(content_type=ct, codename=code)
                      for name, code in perm_codes.items()}

        # ──────────────────────────────────────────────────────────────
        # 2. users
        # ──────────────────────────────────────────────────────────────
        self.viewer = User.objects.create_user("viewer", password="pass")
        self.viewer.user_permissions.add(self.perms["view"])

        self.editor = User.objects.create_user("editor", password="pass")
        self.editor.user_permissions.add(*self.perms.values())     # все четыре

        self.plain = User.objects.create_user("plain", password="pass")  # без прав

        # ──────────────────────────────────────────────────────────────
        # 3. данные
        # ──────────────────────────────────────────────────────────────
        self.status1 = InventoryEquipmentStatus.objects.create(name="Эксплуатация")

        # ──────────────────────────────────────────────────────────────
        # 4. view-handlers
        # ──────────────────────────────────────────────────────────────
        self.list_view = InventoryEquipmentStatusViewSet.as_view({"get": "list"})
        self.create_view = InventoryEquipmentStatusViewSet.as_view({"post": "create"})
        self.detail_view = InventoryEquipmentStatusViewSet.as_view(
            {"patch": "partial_update", "delete": "destroy", "get": "retrieve"}
        )
        self.base_url = "/api/v0/inventory-equipment-status/"

    # ──────────────────────────────────────────────────────────────
    # helpers
    # ──────────────────────────────────────────────────────────────
    def _auth(self, request, user):
        force_authenticate(request, user=user)
        return request

    def _endpoint(self, obj_id):
        return f"{self.base_url}{obj_id}/"

    # ──────────────────────────────────────────────────────────────
    # LIST
    # ──────────────────────────────────────────────────────────────
    def test_list_access(self):
        """
        • Любой аутентифицированный пользователь получает 200.
        • Анонимный запрос — 403.
        """

        # viewer с разрешением view → 200
        req_viewer = self._auth(self.factory.get(self.base_url), self.viewer)
        self.assertEqual(self.list_view(req_viewer).status_code, status.HTTP_200_OK)

        # plain пользователь (без специальных perm) тоже 200
        req_plain = self._auth(self.factory.get(self.base_url), self.plain)
        self.assertEqual(self.list_view(req_plain).status_code, status.HTTP_200_OK)

        # аноним — 403
        anon_resp = self.list_view(self.factory.get(self.base_url))
        self.assertEqual(anon_resp.status_code, status.HTTP_403_FORBIDDEN)

    # ──────────────────────────────────────────────────────────────
    # CREATE
    # ──────────────────────────────────────────────────────────────
    def test_create_status_editor_ok(self):
        payload = {"name": "Списан"}
        req = self._auth(self.factory.post(self.base_url, payload, format="json"), self.editor)
        resp = self.create_view(req)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(InventoryEquipmentStatus.objects.filter(name="Списан").exists())

    def test_create_duplicate_case_insensitive(self):
        InventoryEquipmentStatus.objects.create(name="В ремонте")
        payload = {"name": "в РЕМОНТЕ"}
        req = self._auth(self.factory.post(self.base_url, payload, format="json"), self.editor)
        resp = self.create_view(req)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", resp.data)

    # ──────────────────────────────────────────────────────────────
    # PARTIAL UPDATE
    # ──────────────────────────────────────────────────────────────
    def test_partial_update_name(self):
        patch = {"name": "Испытания"}
        url = self._endpoint(self.status1.id)
        req = self._auth(self.factory.patch(url, patch, format="json"), self.editor)
        resp = self.detail_view(req, pk=self.status1.id)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.status1.refresh_from_db()
        self.assertEqual(self.status1.name, "Испытания")

    # ──────────────────────────────────────────────────────────────
    # DESTROY
    # ──────────────────────────────────────────────────────────────
    def test_destroy_by_editor(self):
        url = self._endpoint(self.status1.id)
        req = self._auth(self.factory.delete(url), self.editor)
        resp = self.detail_view(req, pk=self.status1.id)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(InventoryEquipmentStatus.objects.filter(id=self.status1.id).exists())

    def test_destroy_forbidden_without_permission(self):
        url = self._endpoint(self.status1.id)
        req = self._auth(self.factory.delete(url), self.viewer)  # viewer не имеет delete_perm
        resp = self.detail_view(req, pk=self.status1.id)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from apps.locations.models import Location
from api.v0.views.locations.locations import LocationViewSet

User = get_user_model()


class LocationAdminViewSetTest(APITestCase):
    """
    Покрываем права доступа и базовые CRUD-операции для Location:
    list / create / partial_update / destroy.
    """

    def setUp(self):
        self.factory = APIRequestFactory()

        # ────────────────────────────────────────────────────────────────
        # 1. permissions
        # ────────────────────────────────────────────────────────────────
        ct = ContentType.objects.get_for_model(Location)
        self.perm_view   = Permission.objects.get(content_type=ct, codename="view_location")
        self.perm_add    = Permission.objects.get(content_type=ct, codename="add_location")
        self.perm_change = Permission.objects.get(content_type=ct, codename="change_location")
        self.perm_delete = Permission.objects.get(content_type=ct, codename="delete_location")

        # ────────────────────────────────────────────────────────────────
        # 2. users
        # ────────────────────────────────────────────────────────────────
        self.viewer = User.objects.create_user("viewer", password="pass")
        self.viewer.user_permissions.add(self.perm_view)

        self.editor = User.objects.create_user("editor", password="pass")
        self.editor.user_permissions.add(self.perm_view, self.perm_add, self.perm_change)

        self.admin = User.objects.create_user("admin", password="pass")
        self.admin.user_permissions.add(
            self.perm_view, self.perm_add, self.perm_change, self.perm_delete
        )

        self.plain = User.objects.create_user("plain", password="pass")  # без прав

        # ────────────────────────────────────────────────────────────────
        # 3. данные
        # ────────────────────────────────────────────────────────────────
        self.loc1 = Location.objects.create(
            name="Склад №1", description="Основной склад"
        )

        # ────────────────────────────────────────────────────────────────
        # 4. view-handlers
        # ────────────────────────────────────────────────────────────────
        self.list_view   = LocationViewSet.as_view({"get":    "list"})
        self.create_view = LocationViewSet.as_view({"post":   "create"})
        self.detail_view = LocationViewSet.as_view({
            "patch":   "partial_update",
            "delete":  "destroy",
            "get":     "retrieve",
        })

        self.base_url = "/api/v0/locations/"

    # -------------------------------------------------------------------
    # helpers
    # -------------------------------------------------------------------
    def _auth(self, req, user):
        force_authenticate(req, user=user)
        return req

    def _endpoint(self, obj_id, suffix=""):
        return f"{self.base_url}{obj_id}/{suffix}"

    # -------------------------------------------------------------------
    # LIST
    # -------------------------------------------------------------------
    def test_list_with_and_without_permission(self):
        """
        Любой аутентифицированный пользователь получает 200,
        а неаутентифицированный — 403.
        """
        # пользователь с view-perm
        req = self._auth(self.factory.get(self.base_url), self.viewer)
        self.assertEqual(self.list_view(req).status_code, status.HTTP_200_OK)

        # пользователь без явных perm — тоже 200
        req_plain = self._auth(self.factory.get(self.base_url), self.plain)
        self.assertEqual(self.list_view(req_plain).status_code, status.HTTP_200_OK)

        # аноним — 403
        anon_resp = self.list_view(self.factory.get(self.base_url))
        self.assertEqual(anon_resp.status_code, status.HTTP_403_FORBIDDEN)

    # -------------------------------------------------------------------
    # CREATE
    # -------------------------------------------------------------------
    def test_create_location_editor_has_permission(self):
        payload = {"name": "Склад №2", "description": "Второй склад"}
        req = self._auth(self.factory.post(self.base_url, payload, format="json"),
                         self.editor)
        resp = self.create_view(req)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Location.objects.filter(name="Склад №2").exists())

    def test_create_forbidden_without_add_permission(self):
        payload = {"name": "NoPerm", "description": "Нет прав"}
        req = self._auth(self.factory.post(self.base_url, payload, format="json"),
                         self.viewer)  # viewer не имеет add_location
        resp = self.create_view(req)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # -------------------------------------------------------------------
    # PARTIAL UPDATE
    # -------------------------------------------------------------------
    def test_partial_update_name(self):
        patch = {"name": "Обновлённый склад"}
        url = self._endpoint(self.loc1.id)
        req = self._auth(self.factory.patch(url, patch, format="json"),
                         self.editor)  # есть change_location
        resp = self.detail_view(req, pk=self.loc1.id)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.loc1.refresh_from_db()
        self.assertEqual(self.loc1.name, "Обновлённый склад")

    # -------------------------------------------------------------------
    # DESTROY
    # -------------------------------------------------------------------
    def test_destroy_by_admin(self):
        url = self._endpoint(self.loc1.id)
        req = self._auth(self.factory.delete(url), self.admin)
        resp = self.detail_view(req, pk=self.loc1.id)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Location.objects.filter(id=self.loc1.id).exists())

    def test_destroy_forbidden_without_permission(self):
        url = self._endpoint(self.loc1.id)
        req = self._auth(self.factory.delete(url), self.viewer)
        resp = self.detail_view(req, pk=self.loc1.id)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

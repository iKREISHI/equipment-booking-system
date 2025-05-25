from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

# ⚠️ исправьте путь, если ViewSet находится в другом модуле
from api.v0.views.users.users import UserAdminViewSet

User = get_user_model()


class UserAdminViewSetTest(APITestCase):
    """
    Проверяем:
    • права доступа (superuser / системный админ / модератор);
    • CRUD-операции (list / create / partial_update / destroy);
    • типичные ошибки валидации (несовпадение паролей при create).
    """

    def setUp(self):
        self.factory = APIRequestFactory()

        # создаём группы, которые проверяет IsSuperuserOrSystemAdmin
        self.sys_admin_group = Group.objects.create(name="Администратор системы")
        self.moderator_group = Group.objects.create(name="Модератор")

        # пользователи разных ролей
        self.superuser = User.objects.create_superuser(
            username="root", password="Pass123!"
        )

        self.sys_admin = User.objects.create_user(
            username="sysadmin", password="Pass123!"
        )
        self.sys_admin.groups.add(self.sys_admin_group)

        self.moderator = User.objects.create_user(
            username="moder", password="Pass123!"
        )
        self.moderator.groups.add(self.moderator_group)

        self.regular_user = User.objects.create_user(
            username="ordinary", password="Pass123!"
        )

        # пользователь, с которым будем работать в update / delete
        self.target_user = User.objects.create_user(
            username="target", password="Pass123!", first_name="Before"
        )

        # готовим view-функции
        self.list_view = UserAdminViewSet.as_view({"get": "list"})
        self.create_view = UserAdminViewSet.as_view({"post": "create"})
        self.detail_view = UserAdminViewSet.as_view(
            {"patch": "partial_update", "delete": "destroy", "get": "retrieve"}
        )

        # базовый URL (для APIRequestFactory сам путь значения не имеет)
        self.base_url = "/api/v0/users/"

    # ───────────────────────────────────────────────────────────────────────
    # helpers
    # ───────────────────────────────────────────────────────────────────────
    def _authenticate(self, request, user):
        """Удобный alias, чтобы не писать force_authenticate каждый раз."""
        force_authenticate(request, user=user)
        return request

    def _assert_forbidden(self, user):
        req = self._authenticate(self.factory.get(self.base_url), user)
        resp = self.list_view(req)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # ───────────────────────────────────────────────────────────────────────
    # permissions & list
    # ───────────────────────────────────────────────────────────────────────
    def test_list_permissions(self):
        """Superuser, system-admin и moderator получают 200, остальные 403."""
        for ok_user in (self.superuser, self.sys_admin, self.moderator):
            req = self._authenticate(self.factory.get(self.base_url), ok_user)
            resp = self.list_view(req)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            self.assertIn("results", resp.data)

        # обычный и анонимный — Forbidden
        self._assert_forbidden(self.regular_user)
        anon_resp = self.list_view(self.factory.get(self.base_url))
        self.assertEqual(anon_resp.status_code, status.HTTP_403_FORBIDDEN)

    # ───────────────────────────────────────────────────────────────────────
    # create
    # ───────────────────────────────────────────────────────────────────────
    def test_create_user_by_superuser(self):
        payload = {
            "username": "newbie",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "Иван",
            "last_name": "Иванов",
            "gender": "M",
            "email": "ivan@example.com",
        }

        req = self._authenticate(
            self.factory.post(self.base_url, payload, format="json"), self.superuser
        )
        resp = self.create_view(req)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["username"], payload["username"])

        created = User.objects.get(username="newbie")
        self.assertFalse(created.is_active)  # регистрацию делаем неактивной

    def test_create_password_mismatch_returns_400(self):
        bad_payload = {
            "username": "fail",
            "password": "StrongPass123!",
            "password2": "OtherPass!",
            "first_name": "Test",
            "last_name": "User",
            "gender": "M",
        }
        req = self._authenticate(
            self.factory.post(self.base_url, bad_payload, format="json"), self.superuser
        )
        resp = self.create_view(req)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password2", resp.data)

    # ───────────────────────────────────────────────────────────────────────
    # partial_update
    # ───────────────────────────────────────────────────────────────────────
    def test_partial_update_first_name(self):
        patch_data = {"first_name": "After"}

        req = self._authenticate(
            self.factory.patch(
                f"{self.base_url}{self.target_user.id}/", patch_data, format="json"
            ),
            self.sys_admin,
        )
        resp = self.detail_view(req, pk=self.target_user.id)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.target_user.refresh_from_db()
        self.assertEqual(self.target_user.first_name, "After")

    # ───────────────────────────────────────────────────────────────────────
    # destroy
    # ───────────────────────────────────────────────────────────────────────
    def test_destroy_user_by_moderator(self):
        req = self._authenticate(
            self.factory.delete(f"{self.base_url}{self.target_user.id}/"),
            self.moderator,
        )
        resp = self.detail_view(req, pk=self.target_user.id)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.target_user.id).exists())

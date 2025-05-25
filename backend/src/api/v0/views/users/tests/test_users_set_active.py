from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from api.v0.views.users.users import UserAdminViewSet


User = get_user_model()


class UserAdminSetActiveTest(APITestCase):
    """Тесты detail-action PATCH /users/{id}/set-active/."""

    def setUp(self):
        self.factory = APIRequestFactory()

        # ──────────────────────────────────────────────────────────────────
        # 1. Группы и permissions
        # ──────────────────────────────────────────────────────────────────
        ct_user = ContentType.objects.get_for_model(User)
        all_perms = Permission.objects.filter(
            content_type=ct_user,
            codename__in=["view_user", "add_user", "change_user", "delete_user"],
        )

        self.sys_admin_group = Group.objects.create(name="Администратор системы")
        self.sys_admin_group.permissions.set(all_perms)

        self.moderator_group = Group.objects.create(name="Модератор")
        self.moderator_group.permissions.set(all_perms)

        # ──────────────────────────────────────────────────────────────────
        # 2. Пользователи разных ролей
        # ──────────────────────────────────────────────────────────────────
        self.superuser = User.objects.create_superuser("root", password="Pass123!")

        self.sys_admin = User.objects.create_user("sysadmin", password="Pass123!")
        self.sys_admin.groups.add(self.sys_admin_group)

        self.moderator = User.objects.create_user("moder", password="Pass123!")
        self.moderator.groups.add(self.moderator_group)

        self.regular = User.objects.create_user("ordinary", password="Pass123!")
        # дадим change_user perm без группы
        change_perm = Permission.objects.get(content_type=ct_user, codename="change_user")
        self.regular.user_permissions.add(change_perm)

        # ──────────────────────────────────────────────────────────────────
        # 3. Целевой пользователь
        # ──────────────────────────────────────────────────────────────────
        self.target = User.objects.create_user("target", password="Pass123!", is_active=True)

        # ──────────────────────────────────────────────────────────────────
        # 4. View-функция для экшена set-active
        # ──────────────────────────────────────────────────────────────────
        self.set_active_view = UserAdminViewSet.as_view({"patch": "set_active"})
        self.url = "/api/v0/users/"  # базовый URL (для APIRequestFactory не важен)

    # ──────────────────────────────────────────────────────────────────────
    # helpers
    # ──────────────────────────────────────────────────────────────────────
    def _auth(self, request, user):
        force_authenticate(request, user=user)
        return request

    def _endpoint(self, user_id):
        return f"{self.url}{user_id}/set-active/"

    # ──────────────────────────────────────────────────────────────────────
    # SUCCESS CASES
    # ──────────────────────────────────────────────────────────────────────
    def test_set_active_false_by_superuser(self):
        """
        Суперпользователь может отключить учётку.
        """
        req = self._auth(
            self.factory.patch(self._endpoint(self.target.id), {"is_active": False}, format="json"),
            self.superuser,
        )
        resp = self.set_active_view(req, pk=self.target.id)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.target.refresh_from_db()
        self.assertFalse(self.target.is_active)

    def test_set_active_true_by_sys_admin(self):
        """
        Системный админ включает пользователя.
        """
        # сперва отключим
        self.target.is_active = False
        self.target.save(update_fields=["is_active"])

        req = self._auth(
            self.factory.patch(self._endpoint(self.target.id), {"is_active": True}, format="json"),
            self.sys_admin,
        )
        resp = self.set_active_view(req, pk=self.target.id)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.target.refresh_from_db()
        self.assertTrue(self.target.is_active)

    # ──────────────────────────────────────────────────────────────────────
    # VALIDATION
    # ──────────────────────────────────────────────────────────────────────
    def test_set_active_validation_error(self):
        """
        Отсутствие required-поля is_active → 400 и ошибка валидации.
        """
        req = self._auth(
            self.factory.patch(self._endpoint(self.target.id), {}, format="json"),
            self.superuser,
        )
        resp = self.set_active_view(req, pk=self.target.id)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("is_active", resp.data)

    # ──────────────────────────────────────────────────────────────────────
    # PERMISSIONS
    # ──────────────────────────────────────────────────────────────────────
    def test_set_active_forbidden_for_regular_even_with_change_perm(self):
        """
        Пользователь без нужной группы получает 403,
        даже если у него есть permission change_user.
        """
        req = self._auth(
            self.factory.patch(self._endpoint(self.target.id), {"is_active": False}, format="json"),
            self.regular,
        )
        resp = self.set_active_view(req, pk=self.target.id)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

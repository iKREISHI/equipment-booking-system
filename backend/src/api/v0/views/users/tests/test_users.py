from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

# ⚠️ проверьте импорт, путь зависит от вашего проекта
from api.v0.views.users.users import UserAdminViewSet

User = get_user_model()


class UserAdminViewSetTest(APITestCase):
    """
    Проверяем, что для всех операций требуется:
    1) аутентификация,
    2) нужная model-permission (view / add / change / delete),
    3) принадлежность к группе «Администратор системы» или «Модератор»
       (или superuser).
    """

    def setUp(self):
        self.factory = APIRequestFactory()

        # ------------------------------------------------------------------
        # создаём группы и даём им полный набор model-permissions
        # ------------------------------------------------------------------
        self.ct_user = ContentType.objects.get_for_model(User)
        self.all_perms = Permission.objects.filter(
            content_type=self.ct_user,
            codename__in=["view_user", "add_user", "change_user", "delete_user"],
        )

        self.sys_admin_group = Group.objects.create(name="Администратор системы")
        self.sys_admin_group.permissions.set(self.all_perms)

        self.moderator_group = Group.objects.create(name="Модератор")
        self.moderator_group.permissions.set(self.all_perms)

        # ------------------------------------------------------------------
        # пользователи разных ролей
        # ------------------------------------------------------------------
        self.superuser = User.objects.create_superuser("root", password="Pass123!")

        self.sys_admin = User.objects.create_user("sysadmin", password="Pass123!")
        self.sys_admin.groups.add(self.sys_admin_group)

        self.moderator = User.objects.create_user("moder", password="Pass123!")
        self.moderator.groups.add(self.moderator_group)

        # обычный пользователь: дадим ему *view_user*, но без нужной группы
        self.regular = User.objects.create_user("ordinary", password="Pass123!")
        view_perm = Permission.objects.get(
            content_type=self.ct_user, codename="view_user"
        )
        self.regular.user_permissions.add(view_perm)

        # пользователь-цель для update / delete
        self.target = User.objects.create_user("target", password="Pass123!")

        # ------------------------------------------------------------------
        # готовим view-ручки
        # ------------------------------------------------------------------
        self.list_view = UserAdminViewSet.as_view({"get": "list"})
        self.create_view = UserAdminViewSet.as_view({"post": "create"})
        self.detail_view = UserAdminViewSet.as_view(
            {"patch": "partial_update", "delete": "destroy", "get": "retrieve"}
        )

        self.base_url = "/api/v0/users/"

    # ────────────────────────────────────────────────────────────────────
    # helpers
    # ────────────────────────────────────────────────────────────────────
    def _auth(self, req, user):
        force_authenticate(req, user=user)
        return req

    def _assert_forbidden(self, user, method="get", url=None):
        url = url or self.base_url
        req = self._auth(getattr(self.factory, method)(url), user)
        resp = (self.list_view if method == "get" else self.detail_view)(req)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # ────────────────────────────────────────────────────────────────────
    # list (GET /users/)
    # ────────────────────────────────────────────────────────────────────
    def test_list_permissions(self):
        for ok_user in (self.superuser, self.sys_admin, self.moderator):
            req = self._auth(self.factory.get(self.base_url), ok_user)
            resp = self.list_view(req)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            self.assertIn("results", resp.data)

        # обычный с model-perm, но БЕЗ группы ⇒ 403
        self._assert_forbidden(self.regular)

        # аноним ⇒ 403
        resp = self.list_view(self.factory.get(self.base_url))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # ────────────────────────────────────────────────────────────────────
    # create (POST /users/)
    # ────────────────────────────────────────────────────────────────────
    def test_create_by_sys_admin(self):
        payload = {
            "username": "newbie",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "Иван",
            "last_name": "Иванов",
            "gender": "M",
        }
        req = self._auth(self.factory.post(self.base_url, payload, format="json"),
                         self.sys_admin)
        resp = self.create_view(req)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newbie").exists())

    def test_create_password_mismatch_returns_400(self):
        """
        Пароли разной длины/значения → 400 и ошибка в password2.
        Оба пароля должны удовлетворять validate_password, иначе
        ответ содержит ошибку по полю password (длина ≤ 8 символов).
        """
        bad_payload = {
            "username": "fail",
            "password": "StrongPass123!",        # ≥ 8 символов
            "password2": "DifferentPass123!",    # тоже ≥ 8, но не совпадает
            "first_name": "Test",
            "last_name": "User",
            "gender": "M",
        }

        req = self._auth(
            self.factory.post(self.base_url, bad_payload, format="json"),
            self.superuser,
        )
        resp = self.create_view(req)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password2", resp.data)

    # ────────────────────────────────────────────────────────────────────
    # partial_update (PATCH /users/{id}/)
    # ────────────────────────────────────────────────────────────────────
    def test_partial_update_by_moderator(self):
        patch = {"first_name": "Updated"}
        url = f"{self.base_url}{self.target.id}/"
        req = self._auth(self.factory.patch(url, patch, format="json"),
                         self.moderator)
        resp = self.detail_view(req, pk=self.target.id)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.target.refresh_from_db()
        self.assertEqual(self.target.first_name, "Updated")

    # ────────────────────────────────────────────────────────────────────
    # destroy (DELETE /users/{id}/)
    # ────────────────────────────────────────────────────────────────────
    def test_destroy_by_sys_admin(self):
        url = f"{self.base_url}{self.target.id}/"
        req = self._auth(self.factory.delete(url), self.sys_admin)
        resp = self.detail_view(req, pk=self.target.id)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.target.id).exists())

    def test_destroy_forbidden_for_regular_even_with_perm(self):
        """Есть delete_user perm, но нет группы ⇒ доступ должен быть закрыт."""
        del_perm = Permission.objects.get(
            content_type=self.ct_user, codename="delete_user"
        )
        self.regular.user_permissions.add(del_perm)

        url = f"{self.base_url}{self.target.id}/"
        req = self._auth(self.factory.delete(url), self.regular)
        resp = self.detail_view(req, pk=self.target.id)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

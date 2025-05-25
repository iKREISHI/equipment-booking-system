from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from api.v0.views.users.registration import RegistrationViewSet  # поправьте импорт под свой путь

User = get_user_model()


class RegistrationViewSetTest(APITestCase):
    """
    Тесты эндпоинта POST /register/ (RegistrationViewSet.create)
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = RegistrationViewSet.as_view({'post': 'create'})
        self.url = '/api/v0/register/'  # реальный URL не критичен для APIRequestFactory

        # базовый валидный payload
        self.valid_payload = {
            "username": "new_user",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
            "last_name": "Иванов",
            "first_name": "Иван",
            "gender": "M",
            "email": "ivan@example.com",
        }

    # ──────────────────────────────────────────────────────────────────────────────
    # Positive case
    # ──────────────────────────────────────────────────────────────────────────────
    def test_successful_registration(self):
        """
        Корректные данные → 201 CREATED, пользователь создан и не активен.
        """
        request = self.factory.post(self.url, self.valid_payload, format="json")
        response = self.view(request)

        # HTTP-код и тело ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["detail"],
            "Регистрация прошла успешно. Подтвердите e-mail."
        )

        # пользователь реально создан
        user_id = response.data["user_id"]
        user = User.objects.get(id=user_id)
        self.assertEqual(user.username, self.valid_payload["username"])
        self.assertFalse(user.is_active)                # создали как inactive
        self.assertTrue(user.check_password("StrongPass123!"))  # пароль захеширован

    # ──────────────────────────────────────────────────────────────────────────────
    # Negative cases
    # ──────────────────────────────────────────────────────────────────────────────
    def test_password_mismatch_returns_400(self):
        payload = self.valid_payload | {"password2": "OtherPass999"}
        request = self.factory.post(self.url, payload, format="json")
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password2", response.data)
        self.assertIn("Пароли не совпадают", str(response.data["password2"][0]))

    def test_missing_required_fields_returns_400(self):
        request = self.factory.post(self.url, {}, format="json")
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # username / password / password2 обязательны
        self.assertIn("username", response.data)
        self.assertIn("password", response.data)
        self.assertIn("password2", response.data)

    def test_duplicate_username_returns_400(self):
        """
        Повторная регистрация с тем же username должна вернуть 400.
        """
        # первая (валидная) регистрация
        first_req = self.factory.post(self.url, self.valid_payload, format="json")
        self.view(first_req)

        # вторая с тем же username
        second_req = self.factory.post(self.url, self.valid_payload, format="json")
        second_resp = self.view(second_req)

        self.assertEqual(second_resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", second_resp.data)

from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase

from api.v0.views.users.login import LoginViewSet

User = get_user_model()


class LoginViewSetTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = LoginViewSet.as_view({'post': 'create'})
        self.url = '/api/v0/login/'
        self.username = 'testuser'
        self.password = 'TestPass123!'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

    def _add_session(self, request):
        """Прикручиваем полноценную сессию к request из APIRequestFactory."""
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

    def test_authenticated_user_cannot_login(self):
        request = self.factory.post(self.url, {}, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'detail': 'Вы уже авторизованы'})

    def test_successful_login(self):
        data = {'username': self.username, 'password': self.password}
        request = self.factory.post(self.url, data, format='json')
        # добавляем настоящую сессию
        self._add_session(request)

        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Успешный вход')
        self.assertEqual(response.data['user_id'], self.user.id)
        self.assertEqual(response.data['username'], self.username)

    def test_invalid_credentials(self):
        data = {'username': self.username, 'password': 'wrongpass'}
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)  # ошибок должно быть ≥1

    def test_missing_fields_returns_errors(self):
        request = self.factory.post(self.url, {}, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)
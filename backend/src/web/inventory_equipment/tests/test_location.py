from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, AnonymousUser
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import HttpResponseRedirect, Http404

from web.inventory_equipment.views.location import (
    LocationListView,
    LocationCreateView,
    LocationUpdateView,
    LocationDeleteView,
)
from apps.locations.models import Location  # модель ваших локаций

User = get_user_model()


class LocationURLResolvingTests(TestCase):
    """
    Проверяем, что каждый URL резолвится в свой класс-вью и имеет ожидаемое имя.
    """

    def test_list_url_resolves_to_list_view(self):
        url = reverse('location_list')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, LocationListView)

    def test_create_url_resolves_to_create_view(self):
        url = reverse('location_create')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, LocationCreateView)

    def test_update_url_resolves_to_update_view(self):
        dummy_pk = 1
        url = reverse('location_update', kwargs={'pk': dummy_pk})
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, LocationUpdateView)

    def test_delete_url_resolves_to_delete_view(self):
        dummy_pk = 1
        url = reverse('location_delete', kwargs={'pk': dummy_pk})
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, LocationDeleteView)


class LocationPermissionAndLoginTests(TestCase):
    """
    Проверяем поведение вьюх с точки зрения логина и прав, без рендеринга шаблонов.
    """

    def setUp(self):
        self.factory = RequestFactory()
        # Тестовый пользователь (без любых прав)
        self.user = User.objects.create_user(username='testuser', password='pass')
        # Анонимный пользователь
        self.anonymous = AnonymousUser()

        # Создаём объект Location, чтобы иметь pk
        # Если в модели Location есть другие обязательные поля, добавьте их здесь
        self.location = Location.objects.create(name='Test Location')

        # Строим URL-ы через reverse
        self.url_list   = reverse('location_list')
        self.url_create = reverse('location_create')
        self.url_update = reverse('location_update', kwargs={'pk': self.location.pk})
        self.url_delete = reverse('location_delete', kwargs={'pk': self.location.pk})
        # URL логина
        self.login_url = reverse('login')

    # ---------- ListView Tests ----------

    def test_list_view_redirects_to_login_if_not_authenticated(self):
        """
        GET /location/ без логина → редирект на логин.
        """
        request = self.factory.get(self.url_list)
        request.user = self.anonymous

        response = LocationListView.as_view()(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        expected_redirect = f"{self.login_url}?next={self.url_list}"
        self.assertEqual(response.url, expected_redirect)

    def test_list_view_accessible_for_authenticated_user(self):
        """
        GET /location/ при логине без специальных прав → 200 OK.
        """
        request = self.factory.get(self.url_list)
        request.user = self.user

        response = LocationListView.as_view()(request)
        # Проверяем, что не выброшено исключение и вернулся код 200
        self.assertEqual(response.status_code, 200)

    # ---------- CreateView Tests ----------

    def test_create_view_redirects_to_login_if_not_authenticated(self):
        """
        GET /location/create/ без логина → редирект на логин.
        """
        request = self.factory.get(self.url_create)
        request.user = self.anonymous

        response = LocationCreateView.as_view()(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        expected_redirect = f"{self.login_url}?next={self.url_create}"
        self.assertEqual(response.url, expected_redirect)

    def test_create_view_forbidden_for_user_without_permission(self):
        """
        GET /location/create/ при логине без права add_location → PermissionDenied.
        """
        request = self.factory.get(self.url_create)
        request.user = self.user  # нет права

        with self.assertRaises(PermissionDenied):
            LocationCreateView.as_view()(request)

    def test_create_view_accessible_for_user_with_permission(self):
        """
        GET /location/create/ при праве add_location → 200 OK + в context_data 'form'.
        """
        perm = Permission.objects.get(codename='add_location')
        self.user.user_permissions.add(perm)

        request = self.factory.get(self.url_create)
        request.user = self.user

        response = LocationCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)

    # ---------- UpdateView Tests ----------

    def test_update_view_redirects_to_login_if_not_authenticated(self):
        """
        GET /location/update/<pk>/ без логина → редирект на логин.
        """
        request = self.factory.get(self.url_update)
        request.user = self.anonymous

        response = LocationUpdateView.as_view()(request, pk=self.location.pk)
        self.assertIsInstance(response, HttpResponseRedirect)
        expected_redirect = f"{self.login_url}?next={self.url_update}"
        self.assertEqual(response.url, expected_redirect)

    def test_update_view_forbidden_for_user_without_permission(self):
        """
        GET /location/update/<pk>/ при логине без change_location → PermissionDenied.
        """
        request = self.factory.get(self.url_update)
        request.user = self.user  # нет права

        with self.assertRaises(PermissionDenied):
            LocationUpdateView.as_view()(request, pk=self.location.pk)

    def test_update_view_returns_404_for_user_with_permission_but_nonexistent(self):
        """
        Если объект удалён, но право есть → Http404 или AttributeError.
        """
        perm = Permission.objects.get(codename='change_location')
        self.user.user_permissions.add(perm)
        # Удаляем объект
        self.location.delete()

        request = self.factory.get(self.url_update)
        request.user = self.user

        with self.assertRaises((Http404, AttributeError)):
            LocationUpdateView.as_view()(request, pk=self.location.pk)

    def test_update_view_accessible_for_user_with_permission_and_existing_object(self):
        """
        GET /location/update/<pk>/ при change_location + объект есть → 200 OK и form.instance == объект.
        """
        # Создаём заново объект, если предыдущий удалили
        self.location = Location.objects.create(name='Another Location')
        self.url_update = reverse('location_update', kwargs={'pk': self.location.pk})

        perm = Permission.objects.get(codename='change_location')
        self.user.user_permissions.add(perm)

        request = self.factory.get(self.url_update)
        request.user = self.user

        response = LocationUpdateView.as_view()(request, pk=self.location.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['form'].instance.pk, self.location.pk)

    # ---------- DeleteView Tests ----------

    def test_delete_view_redirects_to_login_if_not_authenticated(self):
        """
        GET /location/delete/<pk>/ без логина → редирект на логин.
        """
        request = self.factory.get(self.url_delete)
        request.user = self.anonymous

        response = LocationDeleteView.as_view()(request, pk=self.location.pk)
        self.assertIsInstance(response, HttpResponseRedirect)
        expected_redirect = f"{self.login_url}?next={self.url_delete}"
        self.assertEqual(response.url, expected_redirect)

    def test_delete_view_forbidden_for_user_without_permission(self):
        """
        GET /location/delete/<pk>/ при логине без delete_location → PermissionDenied.
        """
        request = self.factory.get(self.url_delete)
        request.user = self.user  # нет права

        with self.assertRaises(PermissionDenied):
            LocationDeleteView.as_view()(request, pk=self.location.pk)

    def test_delete_view_returns_404_for_user_with_permission_but_nonexistent(self):
        """
        Если объект удалён, но право есть → Http404 или AttributeError.
        """
        perm = Permission.objects.get(codename='delete_location')
        self.user.user_permissions.add(perm)
        self.location.delete()

        request = self.factory.get(self.url_delete)
        request.user = self.user

        with self.assertRaises((Http404, AttributeError)):
            LocationDeleteView.as_view()(request, pk=self.location.pk)

    def test_delete_view_accessible_for_user_with_permission_and_existing_object(self):
        """
        GET /location/delete/<pk>/ при delete_location + объект есть → 200 OK и context_data['object'] == объект.
        """
        # Восстанавливаем объект
        self.location = Location.objects.create(name='To Delete')
        self.url_delete = reverse('location_delete', kwargs={'pk': self.location.pk})

        perm = Permission.objects.get(codename='delete_location')
        self.user.user_permissions.add(perm)

        request = self.factory.get(self.url_delete)
        request.user = self.user

        response = LocationDeleteView.as_view()(request, pk=self.location.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object'].pk, self.location.pk)

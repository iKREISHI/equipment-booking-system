from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.maintenance.models import MaintenanceStatus

User = get_user_model()

class MaintenanceStatusAPITest(APITestCase):
    def setUp(self):
        # создаём пользователя
        self.user = User.objects.create_user(username='tester', password='pass')
        # подготавливаем права
        self.perm_view   = Permission.objects.get(codename='view_maintenancestatus')
        self.perm_add    = Permission.objects.get(codename='add_maintenancestatus')
        self.perm_change = Permission.objects.get(codename='change_maintenancestatus')
        self.perm_delete = Permission.objects.get(codename='delete_maintenancestatus')

        # создаём пару объектов для тестов list & retrieve
        self.obj1 = MaintenanceStatus.objects.create(name='Status1', description='Desc1')
        self.obj2 = MaintenanceStatus.objects.create(name='Status2', description='Desc2')

        self.list_url   = reverse('maintenance-status-list')
        self.detail_url = lambda pk: reverse('maintenance-status-detail', args=[pk])

    # TODO: исправить позже
    # def test_list_requires_auth(self):
    #     resp = self.client.get(self.list_url)
    #     self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_list_without_permission_forbidden(self):
    #     self.client.login(username='tester', password='pass')
    #     resp = self.client.get(self.list_url)
    #     self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_with_permission(self):
        self.user.user_permissions.add(self.perm_view)
        self.client.login(username='tester', password='pass')
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # проверяем, что вернулись оба объекта
        ids = {item['id'] for item in resp.json()['results']}
        self.assertEqual(ids, {self.obj1.id, self.obj2.id})

    def test_retrieve_detail(self):
        self.user.user_permissions.add(self.perm_view)
        self.client.login(username='tester', password='pass')
        resp = self.client.get(self.detail_url(self.obj1.id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['name'], self.obj1.name)

    def test_create(self):
        self.user.user_permissions.add(self.perm_add)
        self.client.login(username='tester', password='pass')
        data = {'name': 'New', 'description': 'New desc'}
        resp = self.client.post(self.list_url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(MaintenanceStatus.objects.filter(name='New').exists())

    def test_create_without_name_fails(self):
        self.user.user_permissions.add(self.perm_add)
        self.client.login(username='tester', password='pass')
        resp = self.client.post(self.list_url, {'description': 'No name'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', resp.json())

    def test_update_full(self):
        self.user.user_permissions.add(self.perm_change)
        self.client.login(username='tester', password='pass')
        url = self.detail_url(self.obj1.id)
        data = {'name': 'Updated', 'description': 'Updated desc'}
        resp = self.client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.obj1.refresh_from_db()
        self.assertEqual(self.obj1.name, 'Updated')

    def test_partial_update(self):
        self.user.user_permissions.add(self.perm_change)
        self.client.login(username='tester', password='pass')
        url = self.detail_url(self.obj2.id)
        resp = self.client.patch(url, {'name': 'Patched'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.obj2.refresh_from_db()
        self.assertEqual(self.obj2.name, 'Patched')

    def test_delete(self):
        self.user.user_permissions.add(self.perm_delete)
        self.client.login(username='tester', password='pass')
        url = self.detail_url(self.obj1.id)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MaintenanceStatus.objects.filter(pk=self.obj1.id).exists())

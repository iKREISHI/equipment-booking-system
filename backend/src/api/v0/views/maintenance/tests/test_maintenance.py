from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import timedelta

from apps.maintenance.models.maintenance import Maintenance
from apps.maintenance.models.maintenance_status import MaintenanceStatus
from apps.equipments.models import InventoryEquipment
from apps.locations.models import Location

User = get_user_model()


class MaintenanceAPITest(APITestCase):
    def setUp(self):
        # --- Подготовка пользователей и прав ---
        # Создаём пользователя, который будет использоваться во всех тестах
        self.user = User.objects.create_user(username='tester', password='pass')

        # Получаем необходимые permissions для модели Maintenance
        self.perm_view = Permission.objects.get(codename='view_maintenance')
        self.perm_add = Permission.objects.get(codename='add_maintenance')
        self.perm_change = Permission.objects.get(codename='change_maintenance')
        self.perm_delete = Permission.objects.get(codename='delete_maintenance')

        # --- Подготовка связанных данных для InventoryEquipment ---
        # 1. User, который будет владельцем оборудования (owner)
        self.owner = User.objects.create_user(username='owner_equip', password='ownerpass')
        # 2. Location, обязательное поле у InventoryEquipment
        #    Предположим, что модель Location имеет хотя бы поле `name`
        self.location = Location.objects.create(name='Test Location')
        # 3. Создаём InventoryEquipment с обязательными полями: name, owner, location
        self.equipment = InventoryEquipment.objects.create(
            name='Test Equipment',
            owner=self.owner,
            location=self.location
        )

        # --- Подготовка пользователей для Maintenance ---
        # Пользователь, сообщивший о необходимости обслуживания
        self.reporter = User.objects.create_user(username='reporter_user', password='repass')
        # Пользователь, который будет выполнять обслуживание
        self.assigned = User.objects.create_user(username='assigned_user', password='aspass')

        # --- Создаём статус обслуживания ---
        self.status = MaintenanceStatus.objects.create(
            name='В ремонте',
            description='Оборудование в процессе ремонта'
        )

        # --- Создаём несколько объектов Maintenance для тестов list/retrieve ---
        now = timezone.now()
        self.maintenance1 = Maintenance.objects.create(
            equipment=self.equipment,
            reporter_by=self.reporter,
            assigned_by=self.assigned,
            description='Первичная проверка',
            status=self.status,
            description_updated='',
            start_time=now - timedelta(days=1),
            end_time=now,
        )
        self.maintenance2 = Maintenance.objects.create(
            equipment=self.equipment,
            reporter_by=self.reporter,
            assigned_by=self.assigned,
            description='Повторная проверка',
            status=self.status,
            description_updated='Обновлено описание',
            start_time=now - timedelta(days=2),
            end_time=now - timedelta(days=1, hours=20),
        )

        # URL-ы для list и detail
        self.list_url = reverse('maintenance-list')
        self.detail_url = lambda pk: reverse('maintenance-detail', args=[pk])

    def test_list_requires_auth(self):
        """
        Анонимный пользователь при попытке GET /maintenance-list/ должен получить 401 Unauthorized.
        """
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_without_permission_forbidden(self):
        """
        Залогиненный без view_maintenance должен получить 403 Forbidden на list.
        """
        self.client.login(username='tester', password='pass')
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_with_permission(self):
        """
        Залогиненный с view_maintenance должен получить 200 OK и список Maintenance.
        """
        self.user.user_permissions.add(self.perm_view)
        self.client.login(username='tester', password='pass')
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Проверяем, что в ответе есть оба созданных maintenance
        returned_ids = {item['id'] for item in resp.json()['results']}
        self.assertSetEqual(returned_ids, {self.maintenance1.id, self.maintenance2.id})

    def test_retrieve_detail_requires_auth(self):
        """
        Анонимный при GET detail должен получить 401 Unauthorized.
        """
        resp = self.client.get(self.detail_url(self.maintenance1.id))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_without_permission_forbidden(self):
        """
        Залогиненный без view_maintenance при GET detail должен получить 403 Forbidden.
        """
        self.client.login(username='tester', password='pass')
        resp = self.client.get(self.detail_url(self.maintenance1.id))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_with_permission(self):
        """
        Залогиненный с view_maintenance при GET detail должен получить 200 OK и данные Maintenance.
        """
        self.user.user_permissions.add(self.perm_view)
        self.client.login(username='tester', password='pass')
        resp = self.client.get(self.detail_url(self.maintenance1.id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(data['id'], self.maintenance1.id)
        self.assertEqual(data['description'], self.maintenance1.description)

    def test_create_requires_auth(self):
        """
        Анонимный при POST /maintenance-list/ должен получить 401 Unauthorized.
        """
        now = timezone.now()
        new_data = {
            'equipment': self.equipment.pk,
            'reporter_by': self.reporter.pk,
            'assigned_by': self.assigned.pk,
            'description': 'Новая заявка на обслуживание',
            'status': self.status.pk,
            'description_updated': '',
            'start_time': now.isoformat(),
            'end_time': (now + timedelta(hours=1)).isoformat(),
        }
        resp = self.client.post(self.list_url, new_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_without_permission_forbidden(self):
        """
        Залогиненный без add_maintenance при POST должен получить 403 Forbidden.
        """
        self.client.login(username='tester', password='pass')
        now = timezone.now()
        new_data = {
            'equipment': self.equipment.pk,
            'reporter_by': self.reporter.pk,
            'assigned_by': self.assigned.pk,
            'description': 'Новая заявка на обслуживание',
            'status': self.status.pk,
            'description_updated': '',
            'start_time': now.isoformat(),
            'end_time': (now + timedelta(hours=1)).isoformat(),
        }
        resp = self.client.post(self.list_url, new_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_with_permission(self):
        """
        Залогиненный с add_maintenance при POST должен получить 201 Created.
        """
        self.user.user_permissions.add(self.perm_add)
        self.client.login(username='tester', password='pass')

        now = timezone.now()
        new_data = {
            'equipment': self.equipment.pk,
            'reporter_by': self.reporter.pk,
            'assigned_by': self.assigned.pk,
            'description': 'Новая заявка на обслуживание',
            'status': self.status.pk,
            'description_updated': '',
            'start_time': now.isoformat(),
            'end_time': (now + timedelta(hours=1)).isoformat(),
        }

        resp = self.client.post(self.list_url, new_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Проверяем, что объект появился в БД
        created_id = resp.json()['id']
        self.assertTrue(Maintenance.objects.filter(pk=created_id).exists())

    def test_create_invalid_missing_required_fields(self):
        """
        Залогиненный с add_maintenance при POST без обязательных полей должен получить 400 Bad Request.
        """
        self.user.user_permissions.add(self.perm_add)
        self.client.login(username='tester', password='pass')

        # Пробуем без 'equipment'
        now = timezone.now()
        data_missing_equipment = {
            'reporter_by': self.reporter.pk,
            'assigned_by': self.assigned.pk,
            'description': 'Без оборудования',
            'status': self.status.pk,
            'description_updated': '',
            'start_time': now.isoformat(),
            'end_time': (now + timedelta(hours=1)).isoformat(),
        }
        resp = self.client.post(self.list_url, data_missing_equipment, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('equipment', resp.json())

        # Пробуем без 'start_time'
        data_missing_start = {
            'equipment': self.equipment.pk,
            'reporter_by': self.reporter.pk,
            'assigned_by': self.assigned.pk,
            'description': 'Без времени начала',
            'status': self.status.pk,
            'description_updated': '',
            'end_time': (now + timedelta(hours=1)).isoformat(),
        }
        resp2 = self.client.post(self.list_url, data_missing_start, format='json')
        self.assertEqual(resp2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('start_time', resp2.json())

    def test_update_full_requires_auth_and_perm(self):
        """
        Полное обновление (PUT) требует аутентификации и permission 'change_maintenance'.
        """
        url = self.detail_url(self.maintenance1.id)

        # Анонимный → 401
        now = timezone.now()
        update_data = {
            'equipment': self.equipment.pk,
            'reporter_by': self.reporter.pk,
            'assigned_by': self.assigned.pk,
            'description': 'Обновлённая проверка',
            'status': self.status.pk,
            'description_updated': 'Изменено описание',
            'start_time': now.isoformat(),
            'end_time': (now + timedelta(hours=2)).isoformat(),
        }
        resp_anon = self.client.put(url, update_data, format='json')
        self.assertEqual(resp_anon.status_code, status.HTTP_401_UNAUTHORIZED)

        # Залогиненный без change → 403
        self.client.login(username='tester', password='pass')
        resp_forbidden = self.client.put(url, update_data, format='json')
        self.assertEqual(resp_forbidden.status_code, status.HTTP_403_FORBIDDEN)

        # Залогиненный с change → 200 OK и поля обновились
        self.user.user_permissions.add(self.perm_change)
        resp_ok = self.client.put(url, update_data, format='json')
        self.assertEqual(resp_ok.status_code, status.HTTP_200_OK)
        self.maintenance1.refresh_from_db()
        self.assertEqual(self.maintenance1.description, 'Обновлённая проверка')
        self.assertEqual(self.maintenance1.description_updated, 'Изменено описание')

    def test_partial_update_requires_auth_and_perm(self):
        """
        Частичное обновление (PATCH) требует аутентификации и permission 'change_maintenance'.
        """
        url = self.detail_url(self.maintenance2.id)

        # Анонимный → 401
        patch_data = {'description': 'Частичное изменение'}
        resp_anon = self.client.patch(url, patch_data, format='json')
        self.assertEqual(resp_anon.status_code, status.HTTP_401_UNAUTHORIZED)

        # Залогиненный без change → 403
        self.client.login(username='tester', password='pass')
        resp_forbidden = self.client.patch(url, patch_data, format='json')
        self.assertEqual(resp_forbidden.status_code, status.HTTP_403_FORBIDDEN)

        # Залогиненный с change → 200 OK и только поле description изменилось
        self.user.user_permissions.add(self.perm_change)
        resp_ok = self.client.patch(url, patch_data, format='json')
        self.assertEqual(resp_ok.status_code, status.HTTP_200_OK)
        self.maintenance2.refresh_from_db()
        self.assertEqual(self.maintenance2.description, 'Частичное изменение')

    def test_delete_requires_auth_and_perm(self):
        """
        Удаление (DELETE) требует аутентификации и permission 'delete_maintenance'.
        """
        url = self.detail_url(self.maintenance1.id)

        # Анонимный → 401
        resp_anon = self.client.delete(url)
        self.assertEqual(resp_anon.status_code, status.HTTP_401_UNAUTHORIZED)

        # Залогиненный без delete → 403
        self.client.login(username='tester', password='pass')
        resp_forbidden = self.client.delete(url)
        self.assertEqual(resp_forbidden.status_code, status.HTTP_403_FORBIDDEN)

        # Залогиненный с delete → 204 No Content и объект отсутствует
        self.user.user_permissions.add(self.perm_delete)
        resp_ok = self.client.delete(url)
        self.assertEqual(resp_ok.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Maintenance.objects.filter(pk=self.maintenance1.id).exists())

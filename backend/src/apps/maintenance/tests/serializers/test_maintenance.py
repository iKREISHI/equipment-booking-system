from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from apps.maintenance.models.maintenance import Maintenance
from apps.maintenance.serializers import MaintenanceSerializer
from apps.equipments.models import InventoryEquipment
from apps.locations.models import Location
from apps.maintenance.models.maintenance_status import MaintenanceStatus

User = get_user_model()


class MaintenanceSerializerTest(TestCase):
    def setUp(self):
        # 1) Создаём пользователей для reporter_by, assigned_by и owner (для InventoryEquipment)
        self.owner = User.objects.create_user(
            username='owner_user',
            password='ownerpass'
        )
        self.reporter = User.objects.create_user(
            username='reporter_user',
            password='password123'
        )
        self.assigned = User.objects.create_user(
            username='assigned_user',
            password='password123'
        )

        # 2) Создаём статус обслуживания
        self.status = MaintenanceStatus.objects.create(
            name='В ремонте',
            description='Статус проверки'
        )

        # 3) Создаём Location, необходимый для InventoryEquipment
        #    Убедитесь, что у модели Location есть поле "name" или замените под свои нужды.
        self.location = Location.objects.create(
            name='Test Location'
        )

        # 4) Создаём InventoryEquipment с обязательными полями: name, location, owner
        self.equipment = InventoryEquipment.objects.create(
            name='Test Equipment',
            location=self.location,
            owner=self.owner
        )

        # 5) Формируем базовые корректные данные для MaintenanceSerializer
        now = timezone.now()
        self.valid_data = {
            'equipment': self.equipment.pk,
            'reporter_by': self.reporter.pk,
            'assigned_by': self.assigned.pk,
            'description': 'Проверка оборудования',
            'status': self.status.pk,
            'description_updated': 'Ничего не менялось',
            'start_time': now,
            'end_time': now + timedelta(hours=2),
        }

    def test_serializer_with_valid_data_creates_instance(self):
        """
        Проверяем, что сериализатор с валидными данными создаёт объект Maintenance.
        """
        serializer = MaintenanceSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()

        # Проверяем, что объект сохранён и все поля корректно выставились
        self.assertIsInstance(instance, Maintenance)
        self.assertEqual(instance.equipment, self.equipment)
        self.assertEqual(instance.reporter_by, self.reporter)
        self.assertEqual(instance.assigned_by, self.assigned)
        self.assertEqual(instance.status, self.status)
        self.assertEqual(instance.description, self.valid_data['description'])
        self.assertEqual(instance.description_updated, self.valid_data['description_updated'])
        self.assertEqual(instance.start_time, self.valid_data['start_time'])
        self.assertEqual(instance.end_time, self.valid_data['end_time'])

    def test_serializer_missing_required_field_equipment(self):
        """
        Проверяем, что отсутствие обязательного поля 'equipment' даёт ошибку валидации.
        """
        data = self.valid_data.copy()
        data.pop('equipment')
        serializer = MaintenanceSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('equipment', serializer.errors)

    def test_serializer_missing_required_field_reporter_by(self):
        """
        Проверяем, что отсутствие обязательного поля 'reporter_by' даёт ошибку валидации.
        """
        data = self.valid_data.copy()
        data.pop('reporter_by')
        serializer = MaintenanceSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('reporter_by', serializer.errors)

    def test_serializer_missing_required_field_assigned_by(self):
        """
        Проверяем, что отсутствие обязательного поля 'assigned_by' даёт ошибку валидации.
        """
        data = self.valid_data.copy()
        data.pop('assigned_by')
        serializer = MaintenanceSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('assigned_by', serializer.errors)

    def test_serializer_missing_required_field_status(self):
        """
        Проверяем, что отсутствие обязательного поля 'status' даёт ошибку валидации.
        """
        data = self.valid_data.copy()
        data.pop('status')
        serializer = MaintenanceSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('status', serializer.errors)

    def test_serializer_invalid_time_order(self):
        """
        Проверяем, что если start_time > end_time, сериализатор выдаёт ошибку на поле 'end_time'.
        """
        data = self.valid_data.copy()
        now = timezone.now()
        data['start_time'] = now + timedelta(hours=3)
        data['end_time'] = now + timedelta(hours=1)

        serializer = MaintenanceSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('end_time', serializer.errors)
        self.assertEqual(
            serializer.errors['end_time'][0],
            'Время окончания обслуживания должно быть позже времени начала.'
        )

    def test_optional_description_and_description_updated(self):
        """
        Проверяем, что поля description и description_updated могут быть пустыми или отсутствовать.
        """

        # 1) Оба поля переданы как пустые строки
        data1 = self.valid_data.copy()
        data1['description'] = ''
        data1['description_updated'] = ''
        serializer1 = MaintenanceSerializer(data=data1)
        self.assertTrue(serializer1.is_valid(), serializer1.errors)
        inst1 = serializer1.save()
        self.assertEqual(inst1.description, '')
        self.assertEqual(inst1.description_updated, '')

        # 2) Оба поля переданы как None
        data2 = self.valid_data.copy()
        data2['description'] = None
        data2['description_updated'] = None
        serializer2 = MaintenanceSerializer(data=data2)
        self.assertTrue(serializer2.is_valid(), serializer2.errors)
        inst2 = serializer2.save()
        self.assertIsNone(inst2.description)
        self.assertIsNone(inst2.description_updated)

        # 3) Поля вообще отсутствуют в payload
        data3 = self.valid_data.copy()
        data3.pop('description')
        data3.pop('description_updated')
        serializer3 = MaintenanceSerializer(data=data3)
        self.assertTrue(serializer3.is_valid(), serializer3.errors)
        inst3 = serializer3.save()
        # Если в модели нет дефолтного значения, то будет None
        self.assertTrue(inst3.description is None or inst3.description == '')
        self.assertTrue(inst3.description_updated is None or inst3.description_updated == '')

    def test_serializer_read_only_display_fields_ignored(self):
        """
        Проверяем, что попытка передать в сериализатор поля *_display не вызывает ошибку,
        но они не попадают в validated_data (игнорируются при сохранении).
        """
        data = self.valid_data.copy()
        # Добавляем «display»-поля, хотя они в сериализаторе указаны read_only=True
        data['equipment_display'] = 'Некоторый текст'
        data['reporter_display'] = 'Некоторый текст'
        data['assigned_display'] = 'Некоторый текст'
        data['status_display'] = 'Некоторый текст'

        serializer = MaintenanceSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()

        # У объектов модели нет атрибутов «_display», они игнорируются
        self.assertFalse(hasattr(instance, 'equipment_display'))
        self.assertFalse(hasattr(instance, 'reporter_display'))
        self.assertFalse(hasattr(instance, 'assigned_display'))
        self.assertFalse(hasattr(instance, 'status_display'))

    def test_partial_update_respects_time_validation(self):
        """
        При частичном обновлении сериализатор также должен проверять, что
        end_time > start_time, если оба присутствуют в обновлённых данных.
        """
        # Сначала создаём валидный объект через сериализатор
        serializer = MaintenanceSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()

        # Попробуем частично обновить только end_time так, чтобы стало < start_time
        bad_data = {'end_time': instance.start_time - timedelta(minutes=10)}
        partial_serializer = MaintenanceSerializer(
            instance=instance,
            data=bad_data,
            partial=True
        )
        self.assertFalse(partial_serializer.is_valid())
        self.assertIn('end_time', partial_serializer.errors)

        # А теперь корректный частичный апдейт — end_time остаётся > start_time
        good_data = {'end_time': instance.start_time + timedelta(hours=1)}
        partial_serializer2 = MaintenanceSerializer(
            instance=instance,
            data=good_data,
            partial=True
        )
        self.assertTrue(partial_serializer2.is_valid(), partial_serializer2.errors)
        updated = partial_serializer2.save()
        self.assertEqual(updated.end_time, good_data['end_time'])

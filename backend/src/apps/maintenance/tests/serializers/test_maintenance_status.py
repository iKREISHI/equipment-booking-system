from django.test import TestCase
from rest_framework.exceptions import ValidationError
from apps.maintenance.models import MaintenanceStatus
from apps.maintenance.serializers import MaintenanceStatusSerializer

class MaintenanceStatusSerializerTest(TestCase):

    def setUp(self):
        # Создаём исходный объект для тестов обновления
        self.existing = MaintenanceStatus.objects.create(
            name='Initial Status',
            description='Initial description.'
        )

    def test_serializer_with_valid_data_creates_instance(self):
        """Проверка создания нового MaintenanceStatus через сериализатор с валидными данными."""
        data = {
            'name': 'New Status',
            'description': 'Some description here.'
        }
        serializer = MaintenanceStatusSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        # Проверяем, что объект в БД создан и поля совпадают
        self.assertIsInstance(instance, MaintenanceStatus)
        self.assertEqual(instance.name, data['name'])
        self.assertEqual(instance.description, data['description'])

    def test_serializer_missing_name_raises_error(self):
        """Проверяем, что отсутствие обязательного поля name даёт ошибку валидации."""
        data = {
            'description': 'No name provided.'
        }
        serializer = MaintenanceStatusSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        # name — обязательное поле
        self.assertIn('name', serializer.errors)

    def test_serializer_blank_description_is_valid(self):
        """Проверяем, что пустое описание (blank) считается валидным."""
        data = {
            'name': 'Status With Empty Desc',
            'description': ''
        }
        serializer = MaintenanceStatusSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        self.assertEqual(instance.description, '')

    def test_serializer_description_none_is_valid(self):
        """Проверяем, что description=None (null) тоже валидно."""
        data = {
            'name': 'Status With Null Desc',
            'description': None
        }
        serializer = MaintenanceStatusSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        self.assertIsNone(instance.description)

    def test_serializer_update_changes_fields(self):
        """Проверка обновления существующего экземпляра через сериализатор."""
        update_data = {
            'name': 'Updated Status',
            'description': 'Updated description.'
        }
        serializer = MaintenanceStatusSerializer(
            instance=self.existing,
            data=update_data,
            partial=False
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()
        # Проверяем, что это тот же объект и поля обновились
        self.assertEqual(updated.id, self.existing.id)
        self.assertEqual(updated.name, update_data['name'])
        self.assertEqual(updated.description, update_data['description'])

    def test_serializer_partial_update(self):
        """Частичное обновление: меняем только name, не трогая description."""
        partial_data = {
            'name': 'Partially Updated'
        }
        serializer = MaintenanceStatusSerializer(
            instance=self.existing,
            data=partial_data,
            partial=True
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()
        self.assertEqual(updated.name, partial_data['name'])
        # description осталось без изменений
        self.assertEqual(updated.description, self.existing.description)

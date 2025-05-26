from django.test import TestCase
from apps.locations.models import Location
from apps.locations.serializers.locations import LocationSerializer


class LocationSerializerTest(TestCase):
    """
    Покрываем базовые сценарии:
    • сериализация экземпляра в JSON-словарь;
    • создание / валидация корректных данных;
    • ошибки валидации (отсутствие обязательных полей, превышение длины, попытка
      задать read-only id).
    """

    def setUp(self):
        self.valid_payload = {
            "name": "Склад №1",
            "description": "Основной склад на первом этаже."
        }

    # ─────────────────────────────────────────────────────────────────────
    # SERIALIZATION
    # ─────────────────────────────────────────────────────────────────────
    def test_serialization_of_instance(self):
        loc = Location.objects.create(**self.valid_payload)
        data = LocationSerializer(loc).data

        self.assertEqual(
            set(data.keys()),
            {"id", "name", "description"},        # ожидаемые поля
        )
        self.assertEqual(data["id"], loc.id)
        self.assertEqual(data["name"], loc.name)
        self.assertEqual(data["description"], loc.description)

    # ─────────────────────────────────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────────────────────────────────
    def test_create_valid_location(self):
        serializer = LocationSerializer(data=self.valid_payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        loc = serializer.save()
        self.assertIsInstance(loc, Location)
        self.assertEqual(loc.name, self.valid_payload["name"])
        self.assertEqual(loc.description, self.valid_payload["description"])

    # ─────────────────────────────────────────────────────────────────────
    # VALIDATION ERRORS
    # ─────────────────────────────────────────────────────────────────────
    def test_missing_name_returns_error(self):
        payload = self.valid_payload | {"name": ""}
        serializer = LocationSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_missing_description_returns_error(self):
        payload = self.valid_payload | {"description": ""}
        serializer = LocationSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("description", serializer.errors)

    def test_name_too_long(self):
        """Имя длиной 256 символов должно дать ошибку валидации."""
        payload = self.valid_payload | {"name": "A" * 256}
        serializer = LocationSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        # сообщение локализовано («…не более 255 символов»)
        self.assertIn("не более 255 символов", str(serializer.errors["name"][0]))

    def test_cannot_set_readonly_id(self):
        """
        Read-only-поле `id` игнорируется: сериализатор считается валидным,
        в validated_data его нет, а сохранённый объект получает auto-id.
        """
        payload = self.valid_payload | {"id": 999}
        serializer = LocationSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        loc = serializer.save()
        self.assertNotEqual(loc.id, 999)  # id выдан БД
        self.assertNotIn("id", serializer.validated_data)  # поле отброшено

from django.test import TestCase
from apps.equipments.models import InventoryEquipmentStatus
from apps.equipments.serializers.inventory_equipment_status import (
    InventoryEquipmentStatusSerializer,
)


class InventoryEquipmentStatusSerializerTest(TestCase):
    """Базовые сценарии для InventoryEquipmentStatusSerializer."""

    def setUp(self):
        self.valid_payload = {"name": "В работе"}

    # ─────────────────────────────────────────────────────────────
    # SERIALIZATION
    # ─────────────────────────────────────────────────────────────
    def test_serialization_of_instance(self):
        status = InventoryEquipmentStatus.objects.create(**self.valid_payload)
        data = InventoryEquipmentStatusSerializer(status).data

        self.assertEqual(set(data.keys()), {"id", "name"})
        self.assertEqual(data["id"], status.id)
        self.assertEqual(data["name"], status.name)

    # ─────────────────────────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────────────────────────
    def test_create_valid_status(self):
        serializer = InventoryEquipmentStatusSerializer(data=self.valid_payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        status = serializer.save()
        self.assertIsInstance(status, InventoryEquipmentStatus)
        self.assertEqual(status.name, self.valid_payload["name"])

    # ─────────────────────────────────────────────────────────────
    # VALIDATION: пустое имя
    # ─────────────────────────────────────────────────────────────
    def test_missing_name_error(self):
        serializer = InventoryEquipmentStatusSerializer(data={"name": ""})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    # ─────────────────────────────────────────────────────────────
    # VALIDATION: длина > 64
    # ─────────────────────────────────────────────────────────────
    def test_name_too_long(self):
        long_name = "A" * 65        # 65 > 64
        serializer = InventoryEquipmentStatusSerializer(data={"name": long_name})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertIn(
            "не более 64 символов", str(serializer.errors["name"][0])
        )  # сообщение локализовано

    # ─────────────────────────────────────────────────────────────
    # VALIDATION: уникальность (без учёта регистра)
    # ─────────────────────────────────────────────────────────────
    def test_name_uniqueness_case_insensitive(self):
        InventoryEquipmentStatus.objects.create(name="Архивирован")
        # Пытаемся создать «архивирован» другим регистром
        serializer = InventoryEquipmentStatusSerializer(data={"name": "архивирован"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertIn("уже существует", str(serializer.errors["name"][0]))

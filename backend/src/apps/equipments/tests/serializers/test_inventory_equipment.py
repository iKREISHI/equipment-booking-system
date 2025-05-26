from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from apps.equipments.models.inventory_equipment import InventoryEquipment
from apps.equipments.models.inventory_equipment_status import (
    InventoryEquipmentStatus,
)
from apps.locations.models import Location
from apps.users.models import User
from apps.equipments.serializers.inventory_equipment import (
    InventoryEquipmentSerializer,
)


class InventoryEquipmentSerializerTest(TestCase):
    """Базовые сценарии для InventoryEquipmentSerializer."""

    def setUp(self):
        # связанные объекты
        self.owner = User.objects.create_user("john", password="test123")
        self.status_work = InventoryEquipmentStatus.objects.create(name="В работе")
        self.location = Location.objects.create(
            name="Склад 1", description="Основной склад"
        )

        self.valid_payload = {
            "owner": self.owner.id,
            "status": self.status_work.id,
            "location": self.location.id,
            "name": "Дрель Bosch",
            "inventory_number": "EQ-001",
            "description": "Аккумуляторная дрель",
        }

    # ─────────────────────────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────────────────────────
    def test_create_equipment(self):
        serializer = InventoryEquipmentSerializer(data=self.valid_payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        equip = serializer.save()
        self.assertIsInstance(equip, InventoryEquipment)
        self.assertEqual(equip.owner, self.owner)
        self.assertEqual(equip.status, self.status_work)
        self.assertEqual(equip.location, self.location)
        # human-readable поля появляются при сериализации
        data = InventoryEquipmentSerializer(equip).data
        self.assertEqual(data["owner_username"], "john")
        self.assertEqual(data["status_name"], "В работе")
        self.assertEqual(data["location_name"], "Склад 1")

    # ─────────────────────────────────────────────────────────────
    # REQUIRED FIELDS
    # ─────────────────────────────────────────────────────────────
    def test_missing_required_fields(self):
        serializer = InventoryEquipmentSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn("owner", serializer.errors)
        self.assertIn("location", serializer.errors)
        self.assertIn("name", serializer.errors)
        self.assertIn("inventory_number", serializer.errors)

    # ─────────────────────────────────────────────────────────────
    # UNIQUE inventory_number (case-insensitive)
    # ─────────────────────────────────────────────────────────────
    def test_inventory_number_uniqueness_case_insensitive(self):
        # создаём существующий объект
        InventoryEquipment.objects.create(
            owner=self.owner,
            status=self.status_work,
            location=self.location,
            name="Старый",
            inventory_number="EQ-002",
        )
        payload = self.valid_payload | {"inventory_number": "eq-002"}
        serializer = InventoryEquipmentSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("inventory_number", serializer.errors)

    # ─────────────────────────────────────────────────────────────
    # UPDATE пропускает собственный inventory_number
    # ─────────────────────────────────────────────────────────────
    def test_update_allows_same_inventory_number(self):
        equip = InventoryEquipment.objects.create(
            owner=self.owner,
            status=self.status_work,
            location=self.location,
            name="Перфоратор",
            inventory_number="EQ-003",
        )
        # меняем описание, inventory_number остаётся тем же
        serializer = InventoryEquipmentSerializer(
            instance=equip,
            data={"description": "Новое описание"}, partial=True
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()
        self.assertEqual(updated.description, "Новое описание")

    # ─────────────────────────────────────────────────────────────
    # PHOTO size validation
    # ─────────────────────────────────────────────────────────────
    def test_photo_too_large(self):
        big_file = SimpleUploadedFile(
            "photo.jpg",
            b"a" * (2 * 1024 * 1024 + 1),  # 2 МБ + 1 байт
            content_type="image/jpeg",
        )
        payload = self.valid_payload | {"photo": big_file}
        serializer = InventoryEquipmentSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertIn("photo", serializer.errors)
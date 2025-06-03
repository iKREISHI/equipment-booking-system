from django.core.management.base import BaseCommand
from django.db import transaction
from apps.equipments.models.inventory_equipment_status import InventoryEquipmentStatus
from utils.entrypoints.data.inventory_status import inventory_equipment_status


class Command(BaseCommand):
    help = "Создаёт или обновляет предустановленные локации с требуемыми данными."

    @transaction.atomic
    def handle(self, *args, **options):
        for status in inventory_equipment_status:
            name = status["name"]
            InventoryEquipmentStatus.objects.update_or_create(
                name=name,
            )
        self.stdout.write(self.style.SUCCESS("Статусы инвентарного оборудования успешно созданы или обновлены."))

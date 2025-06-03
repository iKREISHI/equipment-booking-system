from django.core.management.base import BaseCommand
from django.db import transaction
from apps.locations.models import Location
from utils.entrypoints.data.inventory_status import inventory_equipment_status


class Command(BaseCommand):
    help = "Создаёт или обновляет предустановленные локации с требуемыми данными."

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Проходим по списку словарей locations и для каждой записи:
        - Если локация с таким именем уже существует, обновляем её описание.
        - Если не существует, создаём новую локацию.
        """
        for status in inventory_equipment_status:
            name = status["name"]
            Location.objects.update_or_create(
                name=name,
            )
        self.stdout.write(self.style.SUCCESS("Статусы инвентарного оборудования успешно созданы или обновлены."))

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.maintenance.models.maintenance_status import MaintenanceStatus
from utils.entrypoints.data.maintenance_status import maintenance_status


class Command(BaseCommand):
    help = "Создаёт или обновляет предустановленные локации с требуемыми данными."

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Проходим по списку словарей maintenance_status и для каждой записи:
        - Если статус с таким именем уже существует, обновляем её описание.
        - Если не существует, создаём новый статус.
        """
        for status in maintenance_status:
            name = status["name"]
            # Используем update_or_create для создания или обновления
            MaintenanceStatus.objects.update_or_create(
                name=name,
            )
        self.stdout.write(self.style.SUCCESS("Статусы обслуживания успешно созданы или обновлены."))

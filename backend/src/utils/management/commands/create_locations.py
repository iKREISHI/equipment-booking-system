from django.core.management.base import BaseCommand
from django.db import transaction
from apps.locations.models import Location
from utils.entrypoints.data.locations import locations


class Command(BaseCommand):
    help = "Создаёт или обновляет предустановленные локации с требуемыми данными."

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Проходим по списку словарей locations и для каждой записи:
        - Если локация с таким именем уже существует, обновляем её описание.
        - Если не существует, создаём новую локацию.
        """
        for loc in locations:
            name = loc["name"]
            description = loc["description"]
            # Используем update_or_create для создания или обновления
            Location.objects.update_or_create(
                name=name,
                defaults={"description": description}
            )
        self.stdout.write(self.style.SUCCESS("Локации успешно созданы или обновлены."))

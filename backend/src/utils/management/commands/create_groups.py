from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.db import transaction
from utils.entrypoints.data.groups import *
# ------------------------------
# Полные наборы прав по моделям
# ------------------------------


class Command(BaseCommand):
    help = "Создаёт или обновляет предустановленные группы с требуемыми правами."

    @transaction.atomic
    def handle(self, *args, **options):
        # Все существующие права в системе
        all_perms = Permission.objects.all()
        perm_map = {p.codename: p for p in all_perms}

        for group_name, rights in GROUP_DEFINITIONS.items():
            group, _ = Group.objects.get_or_create(name=group_name)

            # ----------------------------------------------
            # Особая логика «Администратор системы» и «Обслуживающий персонал»
            # ----------------------------------------------
            if rights == "ALL":
                group.permissions.set(all_perms)
                self.stdout.write(f"✔︎ «{group_name}» — назначены ВСЕ ({all_perms.count()}) права.")
                continue

            # Для обслуживающего персонала добавляем все view_*, кроме maintenance
            if group_name == "Обслуживающий персонал":
                view_else = Permission.objects.filter(
                    codename__startswith="view_"
                ).exclude(codename__in=[
                    perm.codename for perm in perm_map.values()
                    if perm.codename.startswith("view_maintenance")
                    or perm.codename.startswith("view_maintenancestatus")
                ])
                rights = rights + [p.codename for p in view_else]

            # ----------------------------------------------
            # Преобразуем список codenames → Permission QuerySet
            # Фильтрация защищает от отсутствующих моделей (например Reservation)
            # ----------------------------------------------
            valid_perms = [
                perm_map[codename]
                for codename in rights
                if codename in perm_map    # пропускаем ненайденные
            ]
            group.permissions.set(valid_perms)
            self.stdout.write(
                f"✔︎ «{group_name}» — назначено {len(valid_perms)} прав."
            )

        self.stdout.write(self.style.SUCCESS("Все группы успешно обновлены."))

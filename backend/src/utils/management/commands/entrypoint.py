from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from entrypoints.main import main as entrypoint_main

class Command(BaseCommand):
    help = 'Описание вашей команды entrypoint'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Только показать, что бы было сделано, но не выполнять',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        try:
            # Ваша основная логика:
            if dry_run:
                self.stdout.write(self.style.WARNING('Это dry-run, реальных изменений не будет'))

            entrypoint_main()

            self.stdout.write('Запускаем entrypoint…')
            # from utils import some_startup
            # some_startup.run(dry_run=dry_run)
            self.stdout.write(self.style.SUCCESS('Готово!'))
        except Exception as e:
            raise CommandError(f'Ошибка при выполнении entrypoint: {e}')

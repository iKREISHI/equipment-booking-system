import os
import django

# Установка переменной окружения для конфигурации Django и инициализация приложений
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Константы для суперпользователя
SUPERUSER_USERNAME = 'root'
SUPERUSER_PASSWORD = 'root'

from .users import create_superuser_if_not_exists


def main():
    create_superuser_if_not_exists(SUPERUSER_USERNAME, SUPERUSER_PASSWORD)


if __name__ == '__main__':
    main()
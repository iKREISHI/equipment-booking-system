def create_superuser_if_not_exists(username, password):
    """
    Создает суперпользователя, если он не существует.
    """
    from apps.users.models import User
    try:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password)
            print(f"Суперпользователь '{username}' успешно создан.")
        else:
            print(f"Суперпользователь '{username}' уже существует.")
    except Exception as e:
        print(f"Ошибка при создании суперпользователя: {e}")
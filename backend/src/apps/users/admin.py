from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import User


@admin.register(User)
class CustomUser(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_active',)
    fieldsets = (
        (None, {'fields': (
            'last_name', 'first_name', 'patronymic',
            'username', 'password',
            'email', 'telegram_chat_id'
        )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    readonly_fields = ('id', 'last_login', 'date_joined')
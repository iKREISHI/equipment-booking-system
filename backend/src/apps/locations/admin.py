from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Администрирование модели Location.
    """
    list_display = ('name', 'description')  # Поля для отображения в списке
    search_fields = ('name',)               # Поле для поиска
    list_filter = ()                        # Фильтры (если нужны)
    ordering = ('name',)                    # Сортировка по умолчанию
    fieldsets = (
        (None, {
            'fields': ('name', 'description'),
        }),
    )
from django.contrib import admin

from apps.equipments.models import InventoryEquipment
from apps.equipments.models.inventory_equipment_status import InventoryEquipmentStatus


@admin.register(InventoryEquipmentStatus)
class InventoryEquipmentStatusAdmin(admin.ModelAdmin):
    """
    Администрирование модели InventoryEquipmentStatus.
    """
    list_display = ('name',)     # Поля для отображения в списке
    search_fields = ('name',)    # Поле для поиска
    ordering = ('name',)         # Сортировка по умолчанию
    fieldsets = (
        (None, {
            'fields': ('name',),
        }),
    )

@admin.register(InventoryEquipment)
class InventoryEquipmentAdmin(admin.ModelAdmin):
    """
    Администрирование модели InventoryEquipment.
    """
    list_display = (
        'name',
        'inventory_number',
        'registration_date',
        'status',
        'location',
        'count',
        'owner'
    )
    search_fields = (
        'name',
        'inventory_number',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'status',
        'location',
    )
    readonly_fields = ('registration_date', 'created_at', 'updated_at')
    ordering = ('name',)
    date_hierarchy = 'registration_date'
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'inventory_number',
                'registration_date',
                'photo',
                'description',
                'status',
                'location',
                'count',
                'owner',
            ),
        }),
    )
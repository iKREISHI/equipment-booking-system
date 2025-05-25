from django.contrib import admin
from apps.maintenance.models.maintenance_status import MaintenanceStatus
from apps.maintenance.models.maintence import Maintenance


@admin.register(MaintenanceStatus)
class MaintenanceStatusAdmin(admin.ModelAdmin):
    """
    Администрирование модели MaintenanceStatus.
    """
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ()
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description'),
        }),
    )


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = (
        'equipment',
        'status',
        'reporter_by',
        'assigned_by',
    )
    search_fields = (
        'equipment__name',
        'status__name',
        'reporter_by__username',
        'assigned_by__username',
    )
    list_filter = ('status',)
    ordering = ('-id',)
    fieldsets = (
        (None, {
            'fields': (
                'equipment',
                'reporter_by',
                'assigned_by',
                'description',
                'status',
            ),
        }),
    )
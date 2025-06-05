from django.contrib import admin
from apps.reservations.models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    # Отображаемые поля в списке записей
    list_display = (
        'equipment',
        'renter',
        'assigned_by',
        'start_time',
        'end_time',
        'actual_return_time',
        'location',
    )

    # Фильтры по колонкам
    list_filter = (
        'equipment',
        'renter',
        'assigned_by',
        'location',
        'start_time',
    )

    # Поиск по полям связанных таблиц
    search_fields = (
        'renter__username',
        'renter__first_name',
        'renter__last_name',
        'assigned_by__username',
        'assigned_by__first_name',
        'assigned_by__last_name',
        'equipment__name',
    )

    # Иерархия по дате начала аренды
    date_hierarchy = 'start_time'

    # Поля только для чтения (не редактируемые в админке)
    readonly_fields = ('start_time',)

    # Автозавершение для ForeignKey-полей
    autocomplete_fields = (
        'equipment',
        'renter',
        'assigned_by',
    )

    # Организация полей в форме
    fieldsets = (
        (None, {
            'fields': (
                ('equipment', 'location'),
                ('renter', 'assigned_by'),
                ('start_time', 'end_time'),
                ('actual_return_time',),
                'description',
            ),
        }),
    )


# Регистрация модели вместе с кастомным админ-классом
admin.site.register(Reservation, ReservationAdmin)

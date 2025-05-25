from django.db import models
from django.contrib.auth import get_user_model
from apps.equipments.models.inventory_equipment import InventoryEquipment
from apps.locations.models import Location

User = get_user_model()


class Reservation(models.Model):
    """
        Модель аренды инвентарного оборудования
    """
    equipment = models.ForeignKey(
        InventoryEquipment,
        on_delete=models.PROTECT,
        verbose_name='Оборудование',
    )
    renter = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='rented_equipments',
        verbose_name='Арендатор',
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='assigned_arendas',
        verbose_name='Назначил',
    )
    start_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время начала',
    )
    end_time = models.DateTimeField(
        verbose_name='Время окончания',
    )
    actual_return_time = models.DateTimeField(
        verbose_name='Фактическое время возврата',
        null=True,
        blank=True,
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        verbose_name='Расположение оборудование',
    )
    description = models.TextField(
        verbose_name='Описание аренды',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.equipment} — {self.renter} ({self.start_time.date()})"

    class Meta:
        verbose_name = 'Аренда инвентарного оборудования'
        verbose_name_plural = 'Аренды инвентарного оборудования'

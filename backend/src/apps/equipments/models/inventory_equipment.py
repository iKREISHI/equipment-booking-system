from django.db import models

from apps.equipments.models.inventory_equipment_status import InventoryEquipmentStatus
from apps.locations.models import Location
from apps.users.models import User


class InventoryEquipment(models.Model):
    """Модель инвентарного оборудования"""
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Владелец оборудования',
    )

    name = models.CharField(
        max_length=100,
        verbose_name='Название инвентарного оборудования',
    )

    inventory_number = models.CharField(
        max_length=32,
        verbose_name='Штрихкод оборудования',
    )

    registration_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    photo = models.ImageField(
        upload_to="images/",
        null=True,
        blank=True,
        verbose_name='Фото оборудования',
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание оборудования',
    )

    status = models.ForeignKey(
        InventoryEquipmentStatus,
        on_delete=models.PROTECT,
        verbose_name='Статус оборудования',
        blank=True,
        null=True,
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        verbose_name='Расположение оборудования',
    )

    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания',
        blank=True,
        null=True,
    )

    updated_at = models.DateField(
        auto_now=True,
        verbose_name='Дата обновления',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.name} - {self.inventory_number}"

    class Meta:
        verbose_name = 'Инвентарное оборудование'
        verbose_name_plural = 'Инвентарные оборудования'
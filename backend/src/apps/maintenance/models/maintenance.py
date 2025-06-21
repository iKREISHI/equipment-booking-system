from django.db import models

from apps.equipments.models import InventoryEquipment
from apps.maintenance.models.maintenance_status import MaintenanceStatus
from apps.users.models import User


class Maintenance(models.Model):
    """Модель обслуживания/проверки оборудования"""
    equipment = models.ForeignKey(
        InventoryEquipment,
        on_delete=models.PROTECT,
        verbose_name='Оборудование',
    )
    reporter_by = models.ForeignKey(
       'users.User',
        related_name='maintenance_reporter_by',
        on_delete=models.PROTECT,
        verbose_name='Кто сообщил о проверке оборудования',
    )
    assigned_by = models.ForeignKey(
        'users.User',
        related_name='maintenance_assigned_by',
        on_delete=models.PROTECT,
        verbose_name='Кто проверил исправность оборудования',
    )
    description = models.TextField(
        verbose_name='Описание проверки оборудования',
        blank=True,
        null=True,
    )
    status = models.ForeignKey(
        MaintenanceStatus,
        on_delete=models.PROTECT,
        verbose_name='Статус обслуживания',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания <UNK> <UNK>',
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время обновления',
    )

    description_updated = models.TextField(
        verbose_name='Описание обновления',
        blank=True,
        null=True,
    )

    start_time = models.DateTimeField(
        verbose_name='Дата и время начала обслуживания',
    )

    end_time = models.DateTimeField(
        verbose_name='Дата и время конца обслуживания',
    )

    def __str__(self):
        return f"{self.equipment} - {self.status}"

    class Meta:
        verbose_name = 'Обслуживание оборудования'
        verbose_name_plural = 'Обслуживания оборудования'
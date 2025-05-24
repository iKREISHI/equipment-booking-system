from django.db import models

from apps.equipments.models import InventoryEquipment
from apps.maintenance.models.maintenance_status import MaintenanceStatus
from apps.users.models import User


class Maintenance(models.Model):
    """Модель обслуживания/проверки оборудования"""
    equipment = models.ForeignKey(
        InventoryEquipment,
        on_delete=models.PROTECT,
        verbose_name='Инвентарное оборудование',
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

    def __str__(self):
        return f"{self.equipment} - {self.status}"

    class Meta:
        verbose_name = 'Обслуживание оборудования'
        verbose_name_plural = 'Обслуживания оборудования'
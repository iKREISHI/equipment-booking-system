from django.db import models


class InventoryEquipmentStatus(models.Model):
    name = models.CharField(
        verbose_name='Название статуса оборудования',
        max_length=64,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус инвентарного оборудования'
        verbose_name_plural = 'Статусы инвентарного оборудования'


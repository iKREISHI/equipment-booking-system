from django.db import models


class MaintenanceStatus(models.Model):
    """Статус обслуживания оборудования"""
    name = models.CharField(
        max_length=255,
        verbose_name='Название статуса',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус обслуживания оборудования'
        verbose_name_plural = 'Статусы обслуживания оборудования'



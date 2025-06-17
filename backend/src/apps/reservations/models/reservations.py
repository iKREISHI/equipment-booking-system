from django.db import models
from django.contrib.auth import get_user_model
from apps.equipments.models.inventory_equipment import InventoryEquipment

User = get_user_model()


class Reservation(models.Model):
    """
        Модель аренды оборудования
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
        null=True,
        blank=True,
    )
    start_time = models.DateTimeField(
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
    location = models.CharField(
        max_length=255,
        verbose_name='Расположение',
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name='Описание аренды',
        null=True,
        blank=True,
    )
    STATUS_CHOICES = (
        (0, 'На рассмотрении'),
        (1, 'Отклонено'),
        (2, 'Одобрено'),

    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
        verbose_name='Статус',
        null=True,
        blank=True,
    )

    status_response = models.TextField(
        verbose_name='Причина',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.equipment} — {self.renter} ({self.start_time.date()})"

    class Meta:
        verbose_name = 'Аренда оборудования'
        verbose_name_plural = 'Аренды оборудования'

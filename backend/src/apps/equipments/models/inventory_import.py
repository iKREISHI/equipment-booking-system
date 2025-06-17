from django.db import models
from django.conf import settings


class InventoryImport(models.Model):
    """История Excel-импортов оборудования."""
    STATUS_CHOICES = [
        ("PENDING", "В очереди"),
        ("IN_PROGRESS", "Выполняется"),
        ("SUCCESS", "Завершён"),
        ("FAILED", "Ошибка"),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Кто загрузил",
    )
    file = models.FileField(
        upload_to="uploads/inventory/",
        verbose_name="Файл Excel",
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки",
    )
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default="PENDING",
        verbose_name="Статус",
    )
    rows_created = models.PositiveIntegerField(default=0)
    rows_duplicated = models.PositiveIntegerField(default=0)
    rows_skipped = models.PositiveIntegerField(default=0)
    error = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Импорт оборудования"
        verbose_name_plural = "Импорты оборудования"

    def __str__(self):
        return f"Импорт #{self.pk} — {self.file.name}"

from django.db import models


class Location(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название местоположения',
    )
    description = models.TextField(
        verbose_name='Описание местоположения',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Местоположение оборудования'
        verbose_name_plural = 'Местоположения оборудования'
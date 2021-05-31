from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _


class TodoEntry(models.Model):
    class Statuses(models.IntegerChoices):
        """ Два состояния активности бухгалтерских проводок

        Отсюда:
        https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types
        """
        ENABLE = 1, _('Делается')
        DISABLE = 0, _('Сделано')

    date = models.DateField(default=date.today)
    task = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    status = models.IntegerField(
        choices=Statuses.choices,
        default=Statuses.ENABLE,
    )
    comment = models.CharField(max_length=256)
    creator = models.CharField(max_length=32)

    def __str__(self):
        pass

    def get_description(self):
        pass

    def get_absolute_url(self):
        pass

    def get_status(self):
        return self.Statuses(self.status).label

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

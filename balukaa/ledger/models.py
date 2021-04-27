from datetime import date
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _


class Account(models.Model):
    number = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=128)
    fullName = models.CharField(max_length=256)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'Account {self.number} {self.name}'

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "План счетов"


class Entry(models.Model):

    class EntryType(models.TextChoices):
        """
        Отсюда:
        https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types
        """
        MOVE = '+-', _('Перетекание')
        INCREASE = '++', _('Увеличение')
        DECREASE = '--', _('Уменьшение')

    name = models.CharField(max_length=128)
    date = models.DateField(default=date.today)
    fAccount = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    lAccount = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True, related_name='+')
    entryType = models.CharField(
        max_length=2,
        choices=EntryType.choices,
        default=EntryType.INCREASE,
    )
    summ = models.DecimalField(max_digits=10, decimal_places=2)
    is_enter = models.BooleanField()
    created_at = models.DateTimeField(default=timezone.now)
    updates_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Проводка {self.name} {self.summ} {self.date}'

    class Meta:
        verbose_name = "Проводка"
        verbose_name_plural = "Бухгалтерские проводки"

from django.db import models


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
    name = models.CharField(max_length=128)
    date = models.DateField()
    # entryType = models.EnumField(["Перетекание", "Увеличение", "Уменьшение"])
    summ = models.DecimalField(max_digits=10, decimal_places=2)
    is_enter = models.BooleanField()
    created_at = models.DateTimeField()
    updates_at = models.DateTimeField()

    def __str__(self):
        return f'Проводка {self.name} {self.summ} {self.date}'

    class Meta:
        verbose_name = "Проводка"
        verbose_name_plural = "Бухгалтерские проводки"

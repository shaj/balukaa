from django.db import models


class Account(models.Model):
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=128)
    fullName = models.CharField(max_length=256)
    is_active = models.BooleanField()

    def __str__(self):
        return f'Account number {self.number} {self.name}'

    class Meta:
        # db_table = "accounts"
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

    # def __str__(self):
    #     return f''

    class Meta:
        # db_table = "entries"
        verbose_name = "Проводка"
        verbose_name_plural = "Бухгалтерские проводки"

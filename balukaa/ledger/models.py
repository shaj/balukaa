from datetime import date
import decimal
from pprint import pprint
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _


class Account(models.Model):
    number = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=128)
    fullName = models.CharField(max_length=256)
    is_active = models.BooleanField(default=False)

    def getRefs(self) -> int:
        """
        Подсчет общего количества упоминаний этого счета.
        Для тестов и разработки.

        Returns:
            int: общее количество упоминаний счета
        """
        return Entry.objects.filter(is_enter=True).filter(models.Q(lAccount=self.id) | models.Q(fAccount=self.id)).count()

    def getArrival(self, dateFrom: date, dateTo: date) -> decimal.Decimal:
        """
        Подсчет прихода за период (включительно) по таблице Entry
        для текущего счета.

        Args:
            dateStart (date): Начало периода
            dateEnd (date): Конец периода

        Returns:
            decimal.Decimal: приход за период
        """
        q1 = Entry.objects.filter(models.Q(fAccount=self.id) | models.Q(lAccount=self.id),
                                  is_enter=True, entryType=Entry.EntryType.INCREASE.value,
                                  date__gte=dateFrom, date__lte=dateTo).aggregate(models.Sum('summ'))

        q2 = Entry.objects.filter(lAccount=self.id, is_enter=True,
                                  entryType=Entry.EntryType.MOVE.value,
                                  date__gte=dateFrom, date__lte=dateTo).aggregate(models.Sum('summ'))
        summ = decimal.Decimal('0.00')
        if q1['summ__sum'] is not None:
            summ = q1['summ__sum']
        if q2['summ__sum'] is not None:
            summ += q2['summ__sum']

        return summ

    def getExpence(self, dateFrom: date, dateTo: date) -> decimal.Decimal:
        """
        Подсчет прихода за период (включительно) по таблице Entry
        для текущего счета.

        Args:
            dateStart (date): Начало периода
            dateEnd (date): Конец периода

        Returns:
            decimal.Decimal: приход за период
        """
        q1 = Entry.objects.filter(models.Q(fAccount=self.id) | models.Q(lAccount=self.id),
                                  is_enter=True, entryType=Entry.EntryType.DECREASE.value,
                                  date__gte=dateFrom, date__lte=dateTo).aggregate(models.Sum('summ'))

        q2 = Entry.objects.filter(fAccount=self.id, is_enter=True,
                                  entryType=Entry.EntryType.MOVE.value,
                                  date__gte=dateFrom, date__lte=dateTo).aggregate(models.Sum('summ'))
        summ = decimal.Decimal('0.00')
        if q1['summ__sum'] is not None:
            summ = q1['summ__sum']
        if q2['summ__sum'] is not None:
            summ += q2['summ__sum']

        return summ

    def getRemains(self, dateFrom: date, dateTo: date) -> decimal.Decimal:
        """Подсчет остатка на счете на определенную дату

        Args:
            date (date): Дата, на которую нужно посчитать остаток

        Returns:
            decimal.Decimal: Остаток для отображения
        """
        a = self.getArrival(dateFrom, dateTo)
        e = self.getExpence(dateFrom, dateTo)
        d = {
            'arrival': a,
            'expence': e,
            'balance': a-e,
        }
        return d

    def __str__(self):
        return f'{self.number} {self.name}'

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "План счетов"


class Entry(models.Model):

    class EntryType(models.TextChoices):
        """
        Отсюда:
        https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types
        """
        MOVE = '-+', _('Перетекание')
        INCREASE = '++', _('Увеличение')
        DECREASE = '--', _('Уменьшение')

    name = models.CharField(max_length=128)
    date = models.DateField(default=date.today)
    fAccount = models.ForeignKey(
        Account, on_delete=models.SET_NULL, blank=True, null=True)
    lAccount = models.ForeignKey(
        Account, on_delete=models.SET_NULL, blank=True, null=True, related_name='+')
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
        return f'{self.date} | {self.name} | {self.summ}'

    class Meta:
        verbose_name = "Проводка"
        verbose_name_plural = "Бухгалтерские проводки"

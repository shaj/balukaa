import decimal
from datetime import date

from django.urls import reverse
from django.db import models
from django.utils.formats import date_format
from django.utils.translation import gettext_lazy as _


class TimeStampMixin(models.Model):
    """ Абстрактный класс для использования во всех моделях где нужны created_at и updated_at

    Отсюда:
    https://stackoverflow.com/questions/3429878/automatic-creation-date-for-django-model-form-objects
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LedgerAccount(TimeStampMixin):
    class AccountTypes(models.IntegerChoices):
        """ Три типа бухгалтерских cчетов

        Отсюда:
        https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types
        """
        ACTIVE = +1, _('Активный')
        VARIABLE = 0, _('Изменчивый')
        SOURCE = -1, _('Пассивный')

    number = models.CharField(max_length=2,unique=True)
    name = models.CharField(max_length=32)
    full_name = models.CharField(max_length=64)
    type = models.IntegerField(
        choices=AccountTypes.choices,
        default=AccountTypes.ACTIVE,
    )

    def __str__(self):
        # TODO: переделать на "%s ..." % (self.number, ...)
        return f'{self.number} {self.name}'

    def get_description(self):
        # TODO: переделать на "%s ..." % (self.number, ...)
        return f'Счет: {self.number}, ' \
               f'имя: {self.name}, ' \
               f'тип: {self.get_type()}'

    def get_absolute_url(self):
        return reverse('ledger:account_view', args=[self.number])

    # def get_type(self):
    #     return self.AccountTypes(self.type).label

    def get_type_sign(self):
        if self.type == self.AccountTypes.ACTIVE:
            return 'a'
        elif self.type == self.AccountTypes.VARIABLE:
            return '~'
        elif self.type == self.AccountTypes.SOURCE:
            return 'п'

    def get_refs(self) -> int:
        """ Подсчет общего количества упоминаний этого счета.Для тестов и разработки.

        Returns:
            int: общее количество упоминаний счета
        """
        return LedgerEntry.objects.filter(
            status=LedgerEntry.Statuses.ENABLE
        ).filter(
            models.Q(account_two=self.id) | models.Q(account_one=self.id)
        ).count()

    def get_arrival(self, date_from: date, date_to: date) -> decimal.Decimal:
        """ Подсчет прихода за период (включительно) по журналу проводок для текущего счета.

        Args:
            date_from (date): Начало периода
            date_to (date): Конец периода

        Returns:
            decimal.Decimal: приход за период
        """
        query_one = LedgerEntry.objects.filter(
            models.Q(account_one=self.id) | models.Q(account_two=self.id),
            status=LedgerEntry.Statuses.ENABLE,
            type=LedgerEntry.EntryTypes.RISE.value,
            date__gte=date_from,
            date__lte=date_to
        ).aggregate(models.Sum('amount'))

        query_two = LedgerEntry.objects.filter(
            account_two=self.id,
            status=LedgerEntry.Statuses.ENABLE,
            type=LedgerEntry.EntryTypes.MOVE.value,
            date__gte=date_from,
            date__lte=date_to
        ).aggregate(models.Sum('amount'))

        amount = decimal.Decimal('0.00')
        if query_one['amount__sum'] is not None:
            amount = query_one['amount__sum']
        if query_two['amount__sum'] is not None:
            amount += query_two['amount__sum']
        return amount.quantize(decimal.Decimal("1.00"))

    def get_expense(self, date_from: date, date_to: date) -> decimal.Decimal:
        """ Подсчет расхода за период (включительно) по журналу проводок для текущего счета.

        Args:
            date_from (date): Начало периода
            date_to (date): Конец периода

        Returns:
            decimal.Decimal: приход за период
        """
        query_one = LedgerEntry.objects.filter(
            models.Q(account_one=self.id) | models.Q(account_two=self.id),
            status=LedgerEntry.Statuses.ENABLE,
            type=LedgerEntry.EntryTypes.FALL.value,
            date__gte=date_from, date__lte=date_to
        ).aggregate(models.Sum('amount'))

        query_two = LedgerEntry.objects.filter(
            account_one=self.id,
            status=LedgerEntry.Statuses.ENABLE,
            type=LedgerEntry.EntryTypes.MOVE.value,
            date__gte=date_from,
            date__lte=date_to
        ).aggregate(models.Sum('amount'))

        amount = decimal.Decimal('0.00')
        if query_one['amount__sum'] is not None:
            amount = query_one['amount__sum']
        if query_two['amount__sum'] is not None:
            amount += query_two['amount__sum']

        return amount.quantize(decimal.Decimal("1.00"))

    def get_remains(self, date_from: date, date_to: date) -> decimal.Decimal:
        """Подсчет остатка на счете на определенную дату. НЕ ДОДЕЛАНА!

        Для корректного расчета остатка на счету на дату надо, чтобы считалось не от начальной даты,
        а с начала движений по счету.
        Может быть сделать отдельную функцию для этого.
        Args:
            date_from (date): Дата, с которой начинается расчет приходов/расходов
            date_to (date): Дата, на которую нужно посчитать остаток

        Returns:
            decimal.Decimal: Остаток для отображения
        """
        arrival = self.get_arrival(date_from, date_to)
        expense = self.get_expense(date_from, date_to)
        balance = {
            'arrival': arrival,
            'expense': expense,
            'balance': (arrival - expense),
        }
        return balance

    def get_account_balance(self, date_to: date) -> decimal.Decimal:
        """Подсчет остатка на счете на определенную дату.

        Args:
            date_to (date): Дата, на которую нужно посчитать остаток

        Returns:
            decimal.Decimal: Остаток для отображения
        """
        date_earliest = LedgerEntry.objects.earliest('date').date
        arrival = self.get_arrival(date_earliest, date_to)
        expense = self.get_expense(date_earliest, date_to)
        balance = arrival - expense
        return balance

    class Meta:
        verbose_name = "Бухгалтерский счет"
        verbose_name_plural = "План счетов"


class LedgerEntry(TimeStampMixin):
    class EntryTypes(models.IntegerChoices):
        """ Три вида бухгалтерских проводок

        Отсюда:
        https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types
        """
        RISE = 1, _('Увеличение')
        MOVE = 0, _('Перетекание')
        FALL = -1, _('Уменьшение')

    class Statuses(models.IntegerChoices):
        """ Два состояния активности бухгалтерских проводок

        Отсюда:
        https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types
        """
        ENABLE = 1, _('Включена')
        DISABLE = 0, _('Выключена')

    date = models.DateField(default=date.today)
    account_one = models.ForeignKey(
        LedgerAccount, on_delete=models.SET_NULL, blank=True, null=True)
    account_two = models.ForeignKey(
        LedgerAccount, on_delete=models.SET_NULL, blank=True, null=True, related_name='+')
    type = models.IntegerField(
        choices=EntryTypes.choices,
        default=EntryTypes.RISE,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.CharField(max_length=256)
    status = models.IntegerField(
        choices=Statuses.choices,
        default=Statuses.ENABLE,
    )

    def __str__(self):
        # TODO: переделать на "%s ..." % (self.number, ...)
        return f'id:{self.pk}, ' \
               f"{date_format(self.date, 'SHORT_DATE_FORMAT')}, " \
               f'{self.comment}, ' \
               f'{self.get_account_one_type_symbol()}{self.account_one.number} ' \
               f'{self.get_account_two_type_symbol()}{self.account_two.number}, ' \
               f'{self.amount}, ' \
               f'{self.get_status()}'

    def get_description(self):
        # TODO: переделать на "%s ..." % (self.number, ...)
        return f'Проводка: {self.comment}, ' \
               f'id: {self.pk}, ' \
               f"дата: {date_format(self.date, 'SHORT_DATE_FORMAT')}, " \
               f'счета: {self.get_account_one_type_symbol()}{self.account_one.number} ' \
               f'{self.get_account_two_type_symbol()}{self.account_two.number}, ' \
               f'сумма: {self.amount}, ' \
               f'статус: {self.get_status()}'

    def get_absolute_url(self):
        return reverse('ledger:entry_view', args=[self.pk])

    # def get_type(self):
    #     return self.EntryTypes(self.type).label

    def get_account_one_type_symbol(self):
        if self.type == self.EntryTypes.RISE:
            return '+'
        elif self.type == self.EntryTypes.MOVE or \
                self.type == self.EntryTypes.FALL:
            return '-'

    def get_account_two_type_symbol(self):
        if self.type == self.EntryTypes.RISE or \
                self.type == self.EntryTypes.MOVE:
            return '+'
        elif self.type == self.EntryTypes.FALL:
            return '-'

    def get_status(self):
        return self.Statuses(self.status).label

    class Meta:
        verbose_name = "Бухгалтерская проводка"
        verbose_name_plural = "Бухгалтерские проводки"

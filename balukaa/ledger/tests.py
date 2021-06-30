from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone
from .models import LedgerAccount, LedgerEntry

ACCOUNTS = [
    (50, 'Касса', 'Кассы', LedgerAccount.AccountTypes.ACTIVE),
    (51, 'РСчет', 'Расчетные счета', LedgerAccount.AccountTypes.ACTIVE),
    (60, 'Поставщики', 'Расчеты с поставщиками и подрядчиками', LedgerAccount.AccountTypes.VARIABLE),
    (41, 'Товары', 'Товары для продажи', LedgerAccount.AccountTypes.ACTIVE),
    (62, 'Покупатели', 'Расчеты с покупателями и заказчиками', LedgerAccount.AccountTypes.VARIABLE),
    (66, 'КЗаймы', 'Расчеты по краткосрочным кредитам и займам', LedgerAccount.AccountTypes.SOURCE),
    (67, 'ДЗаймы', 'Расчеты по долгосрочным кредитам и займам', LedgerAccount.AccountTypes.SOURCE),
]


# Create your tests here.
class TestAccounts(TestCase):

    def test_main(self):
        self.assertEqual(LedgerAccount.objects.count(), 0)


class TestEntries(TestCase):

    def setUp(self):
        self.accounts = dict()
        for el in ACCOUNTS:
            self.accounts[str(el[0])] = LedgerAccount.objects.create(
                number=el[0],
                name=el[1],
                full_name=el[2],
                type=el[3]
            )

    def test_main_one(self):
        LedgerEntry.objects.create(
            date=date(2021, 1, 11),
            account_one=self.accounts['50'],  # Касса
            account_two=self.accounts['60'],  # Поставщики
            type=LedgerEntry.EntryTypes.FALL.value,
            amount=500.00,
            status=False
            # created_at=timezone.now(),
            # updated_at=timezone.now(),
        )
        self.assertEqual(LedgerEntry.objects.count(), 1)


ENTRIES1 = [
    (date(2021, 1, 11), '51', '50', LedgerEntry.EntryTypes.MOVE,
     '1100.01', 'Снятие с рсчета в кассу', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 13), '50', '60', LedgerEntry.EntryTypes.FALL,
     '1200.02', 'Оплата из кассы поставщику', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 15), '41', '60', LedgerEntry.EntryTypes.RISE,
     '1300.03', 'Поступление товара от поставщика', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 17), '41', '62', LedgerEntry.EntryTypes.FALL,
     '1400.04', 'Отгрузка товара покупателю', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 19), '51', '50', LedgerEntry.EntryTypes.MOVE,
     '2100.01', 'Снятие с рсчета в кассу', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 21), '50', '60', LedgerEntry.EntryTypes.FALL,
     '2200.02', 'Оплата из кассы поставщику', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 23), '41', '60', LedgerEntry.EntryTypes.RISE,
     '2300.03', 'Поступление товара от поставщика', LedgerEntry.Statuses.ENABLE),
    (date(2021, 2, 10), '41', '62', LedgerEntry.EntryTypes.FALL,
     '2400.04', 'Отгрузка товара покупателю', LedgerEntry.Statuses.ENABLE),
    (date(2021, 2, 12), '51', '50', LedgerEntry.EntryTypes.MOVE,
     '3100.01', 'Снятие с рсчета в кассу', LedgerEntry.Statuses.ENABLE),
    (date(2021, 2, 14), '50', '60', LedgerEntry.EntryTypes.FALL,
     '3200.02', 'Оплата из кассы поставщику', LedgerEntry.Statuses.ENABLE),
    (date(2021, 2, 16), '41', '60', LedgerEntry.EntryTypes.RISE,
     '3300.03', 'Поступление товара от поставщика', LedgerEntry.Statuses.ENABLE),
    (date(2021, 2, 18), '41', '62', LedgerEntry.EntryTypes.FALL,
     '3400.04', 'Отгрузка товара покупателю', LedgerEntry.Statuses.ENABLE),
    (date(2021, 3, 11), '51', '50', LedgerEntry.EntryTypes.MOVE,
     '4100.01', 'Снятие с рсчета в кассу', LedgerEntry.Statuses.ENABLE),
    (date(2021, 3, 13), '50', '60', LedgerEntry.EntryTypes.FALL,
     '4200.02', 'Оплата из кассы поставщику', LedgerEntry.Statuses.ENABLE),
    (date(2021, 3, 15), '41', '60', LedgerEntry.EntryTypes.RISE,
     '4300.03', 'Поступление товара от поставщика', LedgerEntry.Statuses.ENABLE),
    (date(2021, 3, 17), '41', '62', LedgerEntry.EntryTypes.FALL,
     '4400.04', 'Отгрузка товара покупателю', LedgerEntry.Statuses.ENABLE),
]


class TestAccountCard(TestCase):
    """
    Тестирование функций, относящихся к формированию отчета "Карточка счета"
    """

    def setUp(self) -> None:
        self.accounts = dict()
        for el in ACCOUNTS:
            self.accounts[str(el[0])] = LedgerAccount.objects.create(
                number=el[0],
                name=el[1],
                full_name=el[2],
                type=el[3]
            )

    def test_initdb(self):
        for el in ENTRIES1:
            LedgerEntry.objects.create(
                date=el[0],
                account_one=self.accounts[el[1]],
                account_two=self.accounts[el[2]],
                type=el[3],
                amount=el[4],
                comment=el[5],
                status=el[6]
            )

        self.assertEqual(LedgerEntry.objects.count(), len(ENTRIES1))

    def test_empty_entries(self):
        self.assertEqual(LedgerEntry.objects.count(), 0)
        arrival = self.accounts['50'].get_arrival(date(2021, 1, 1), date(2022, 1, 1))
        self.assertEqual(str(arrival), '0.00')
        expense = self.accounts['50'].get_expense(date(2021, 1, 1), date(2022, 1, 1))
        self.assertEqual(str(expense), '0.00')
        balance = self.accounts['50'].get_remains(date(2021, 1, 1), date(2022, 1, 1))
        d = {
            'arrival': Decimal('0.00'),
            'expense': Decimal('0.00'),
            'balance': Decimal('0.00'),
        }
        self.assertDictEqual(balance, d)


class TestACard_Entries1(TestCase):

    def setUp(self) -> None:
        self.accounts = dict()
        for el in ACCOUNTS:
            self.accounts[str(el[0])] = LedgerAccount.objects.create(
                number=el[0],
                name=el[1],
                full_name=el[2],
                type=el[3]
            )
        for el in ENTRIES1:
            LedgerEntry.objects.create(
                date=el[0],
                account_one=self.accounts[el[1]],
                account_two=self.accounts[el[2]],
                type=el[3],
                amount=el[4],
                comment=el[5],
                status=el[6]
            )

    def test_balance_output_format(self):
        arrival = self.accounts['50'].get_arrival(date(2021, 1, 1), date(2022, 1, 1))
        self.assertEqual(str(arrival), '10400.04')
        expense = self.accounts['50'].get_expense(date(2021, 1, 1), date(2022, 1, 1))
        self.assertEqual(str(expense), '10800.08')
        balance = self.accounts['50'].get_remains(date(2021, 1, 1), date(2022, 1, 1))
        self.assertEqual(str(balance['arrival']), '10400.04')
        self.assertEqual(str(balance['expense']), '10800.08')
        self.assertEqual(str(balance['balance']), '-400.04')

    def test_balance(self):
        balance = self.accounts['50'].get_remains(date(2021, 1, 1), date(2022, 1, 1))
        # pprint(balance)
        d = {
            'arrival': Decimal('10400.04'),
            'expense': Decimal('10800.08'),
            'balance': Decimal('-400.04'),
        }
        self.assertDictEqual(balance, d)

    def test_balance_datelimit_50(self):
        balance = self.accounts['50'].get_remains(date(2021, 1, 17), date(2021, 3, 11))
        # pprint(balance)
        d = {
            'arrival': Decimal('9300.03'),
            'expense': Decimal('5400.04'),
            'balance': Decimal('3899.99'),
        }
        self.assertDictEqual(balance, d)

    def test_balance_datelimit_wrong_date(self):
        balance = self.accounts['51'].get_remains(date(2021, 1, 17), date(2021, 1, 1))
        # pprint(balance)
        d = {
            'arrival': Decimal('0.00'),
            'expense': Decimal('0.00'),
            'balance': Decimal('0.00'),
        }
        self.assertDictEqual(balance, d)

    def test_balance_datelimit_zero_summ(self):
        balance = self.accounts['60'].get_remains(date(2021, 1, 16), date(2021, 1, 20))
        # pprint(balance)
        d = {
            'arrival': Decimal('0.00'),
            'expense': Decimal('0.00'),
            'balance': Decimal('0.00'),
        }
        self.assertDictEqual(balance, d)

    def test_balance_datelimit_enother_account(self):
        balance = self.accounts['62'].get_remains(date(2021, 1, 17), date(2021, 3, 11))
        # pprint(balance)
        d = {
            'arrival': Decimal('5600.06'),
            'expense': Decimal('7200.12'),
            'balance': Decimal('-1600.06'),
        }
        self.assertDictEqual(balance, d)


ENTRIES2 = [
    (date(2021, 1, 11), '51', '50', LedgerEntry.EntryTypes.MOVE,
     '1100.01', 'Снятие с рсчета в кассу', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 13), '50', '60', LedgerEntry.EntryTypes.FALL,
     '1200.02', 'Оплата из кассы поставщику', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 15), '41', '60', LedgerEntry.EntryTypes.RISE,
     '1300.03', 'Поступление товара от поставщика', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 17), '41', '62', LedgerEntry.EntryTypes.FALL,
     '1400.04', 'Отгрузка товара покупателю', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 19), '51', '50', LedgerEntry.EntryTypes.MOVE,
     '2100.01', 'Снятие с рсчета в кассу', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 21), '50', '60', LedgerEntry.EntryTypes.FALL,
     '2200.02', 'Оплата из кассы поставщику', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 23), '41', '60', LedgerEntry.EntryTypes.RISE,
     '2300.03', 'Поступление товара от поставщика', LedgerEntry.Statuses.DISABLE),
    (date(2021, 2, 10), '41', '62', LedgerEntry.EntryTypes.FALL,
     '2400.04', 'Отгрузка товара покупателю', LedgerEntry.Statuses.DISABLE),
    (date(2021, 2, 12), '51', '50', LedgerEntry.EntryTypes.MOVE,
     '3100.01', 'Снятие с рсчета в кассу', LedgerEntry.Statuses.DISABLE),
    (date(2021, 2, 14), '50', '60', LedgerEntry.EntryTypes.FALL,
     '3200.02', 'Оплата из кассы поставщику', LedgerEntry.Statuses.DISABLE),
    (date(2021, 2, 16), '41', '60', LedgerEntry.EntryTypes.RISE,
     '3300.03', 'Поступление товара от поставщика', LedgerEntry.Statuses.ENABLE),
    (date(2021, 2, 18), '41', '62', LedgerEntry.EntryTypes.FALL,
     '3400.04', 'Отгрузка товара покупателю', LedgerEntry.Statuses.ENABLE),
    (date(2021, 3, 11), '51', '50', LedgerEntry.EntryTypes.MOVE,
     '4100.01', 'Снятие с рсчета в кассу', LedgerEntry.Statuses.ENABLE),
    (date(2021, 3, 13), '50', '60', LedgerEntry.EntryTypes.FALL,
     '4200.02', 'Оплата из кассы поставщику', LedgerEntry.Statuses.ENABLE),
    (date(2021, 3, 15), '41', '60', LedgerEntry.EntryTypes.RISE,
     '4300.03', 'Поступление товара от поставщика', LedgerEntry.Statuses.ENABLE),
    (date(2021, 3, 17), '41', '62', LedgerEntry.EntryTypes.FALL,
     '4400.04', 'Отгрузка товара покупателю', LedgerEntry.Statuses.ENABLE),
]


class TestACard_Entries2(TestCase):

    def setUp(self) -> None:
        self.accounts = dict()
        for el in ACCOUNTS:
            self.accounts[str(el[0])] = LedgerAccount.objects.create(
                number=el[0],
                name=el[1],
                full_name=el[2],
                type=el[3]
            )
        for el in ENTRIES2:
            LedgerEntry.objects.create(
                date=el[0],
                account_one=self.accounts[el[1]],
                account_two=self.accounts[el[2]],
                type=el[3],
                amount=el[4],
                comment=el[5],
                status=el[6]
            )

    def test_balance_datelimit_51(self):
        balance = self.accounts['51'].get_remains(date(2021, 1, 17), date(2021, 3, 11))
        # pprint(balance)
        d = {
            'arrival': Decimal('0.00'),
            'expense': Decimal('6200.02'),
            'balance': Decimal('-6200.02'),
        }
        self.assertDictEqual(balance, d)

    def test_balance_datelimit_67(self):
        balance = self.accounts['67'].get_remains(date(2021, 1, 17), date(2021, 3, 11))
        # pprint(balance)
        d = {
            'arrival': Decimal('0.00'),
            'expense': Decimal('4800.08'),
            'balance': Decimal('-4800.08'),
        }
        self.assertDictEqual(balance, d)

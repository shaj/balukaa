from datetime import date
from decimal import Decimal
from pprint import pprint

from django.test import TestCase
from django.utils import timezone
from .models import Account, Entry


ACCOUNTS = [
    (50, "Касса", "Касса", True),
    (51, "Рсчет", "Расчетный счет", True),
    (60, "Поставщики", "Расчеты с поставщиками и подрядчиками", False),
    (62, "Товар", "Товар", False),
    (75, "Покупатели", "Расчеты с покупателями", False),
]

# Create your tests here.
class TestAccounts(TestCase):
    def test_main(self):
        self.assertEqual(Account.objects.count(), 0)


class TestEntries(TestCase):
    def setUp(self):
        self.accounts = dict()
        for el in ACCOUNTS:
            self.accounts[str(el[0])] = Account.objects.create(
                number=el[0], name=el[1], fullName=el[2], is_active=el[3]
            )

    def test_main_one(self):
        Entry.objects.create(
            name="Выплата поставщику",
            date=date(2021, 1, 11),
            fAccount=self.accounts["50"],  # Касса
            lAccount=self.accounts["60"],  # Поставщики
            entryType=Entry.EntryType.DECREASE.value,
            summ=500.00,
            is_enter=False,
            created_at=timezone.now(),
            updates_at=timezone.now(),
        )
        self.assertEqual(Entry.objects.count(), 1)


ENTRIES1 = [
    ("Test 1 1", date(2021, 1, 11), "51", "50", "-+", "1100.01", True),
    ("Test 2 1", date(2021, 1, 13), "50", "60", "--", "1200.02", True),
    ("Test 3 1", date(2021, 1, 15), "62", "60", "++", "1300.03", True),
    ("Test 4 1", date(2021, 1, 17), "62", "75", "--", "1400.04", True),
    ("Test 1 2", date(2021, 1, 19), "51", "50", "-+", "2100.01", True),
    ("Test 2 2", date(2021, 1, 21), "50", "60", "--", "2200.02", True),
    ("Test 3 2", date(2021, 1, 23), "62", "60", "++", "2300.03", True),
    ("Test 4 2", date(2021, 2, 10), "62", "75", "--", "2400.04", True),
    ("Test 1 3", date(2021, 2, 12), "51", "50", "-+", "3100.01", True),
    ("Test 2 3", date(2021, 2, 14), "50", "60", "--", "3200.02", True),
    ("Test 3 3", date(2021, 2, 16), "62", "60", "++", "3300.03", True),
    ("Test 4 3", date(2021, 2, 18), "62", "75", "--", "3400.04", True),
    ("Test 1 4", date(2021, 3, 11), "51", "50", "-+", "4100.01", True),
    ("Test 2 4", date(2021, 3, 13), "50", "60", "--", "4200.02", True),
    ("Test 3 4", date(2021, 3, 15), "62", "60", "++", "4300.03", True),
    ("Test 4 4", date(2021, 3, 17), "62", "75", "--", "4400.04", True),
]


class TestAccountCard(TestCase):
    """
    Тестирование функций, относящихся к формированию отчета "Карточка счета"
    """

    def setUp(self) -> None:
        self.accounts = dict()
        for el in ACCOUNTS:
            self.accounts[str(el[0])] = Account.objects.create(
                number=el[0], name=el[1], fullName=el[2], is_active=el[3]
            )

    def test_initdb(self):
        for el in ENTRIES1:
            Entry.objects.create(
                name=el[0],
                date=el[1],
                fAccount=self.accounts[el[2]],
                lAccount=self.accounts[el[3]],
                entryType=el[4],
                summ=el[5],
                is_enter=el[6],
            )

        self.assertEqual(Entry.objects.count(), len(ENTRIES1))

    def test_empty_entries(self):
        self.assertEqual(Entry.objects.count(), 0)
        arrival = self.accounts["50"].getArrival(date(2021, 1, 1), date(2022, 1, 1))
        self.assertEqual(str(arrival), "0.00")
        expence = self.accounts["50"].getExpence(date(2021, 1, 1), date(2022, 1, 1))
        self.assertEqual(str(expence), "0.00")
        balance = self.accounts["50"].getRemains(date(2021, 1, 1), date(2022, 1, 1))
        d = {
            "arrival": Decimal("0.00"),
            "expence": Decimal("0.00"),
            "balance": Decimal("0.00"),
        }
        self.assertDictEqual(balance, d)


class TestACard_Entries1(TestCase):
    def setUp(self) -> None:
        self.accounts = dict()
        for el in ACCOUNTS:
            self.accounts[str(el[0])] = Account.objects.create(
                number=el[0], name=el[1], fullName=el[2], is_active=el[3]
            )
        for el in ENTRIES1:
            Entry.objects.create(
                name=el[0],
                date=el[1],
                fAccount=self.accounts[el[2]],
                lAccount=self.accounts[el[3]],
                entryType=el[4],
                summ=el[5],
                is_enter=el[6],
            )

    def test_balance_output_format(self):
        arrival = self.accounts["50"].getArrival(date(2021, 1, 1), date(2022, 1, 1))
        self.assertEqual(str(arrival), "10400.04")
        expence = self.accounts["50"].getExpence(date(2021, 1, 1), date(2022, 1, 1))
        self.assertEqual(str(expence), "10800.08")
        balance = self.accounts["50"].getRemains(date(2021, 1, 1), date(2022, 1, 1))
        self.assertEqual(str(balance["arrival"]), "10400.04")
        self.assertEqual(str(balance["expence"]), "10800.08")
        self.assertEqual(str(balance["balance"]), "-400.04")

    def test_balance(self):
        balance = self.accounts["50"].getRemains(date(2021, 1, 1), date(2022, 1, 1))
        # pprint(balance)
        d = {
            "arrival": Decimal("10400.04"),
            "expence": Decimal("10800.08"),
            "balance": Decimal("-400.04"),
        }
        self.assertDictEqual(balance, d)

    def test_balance_datelimit_50(self):
        balance = self.accounts["50"].getRemains(date(2021, 1, 17), date(2021, 3, 11))
        # pprint(balance)
        d = {
            "arrival": Decimal("9300.03"),
            "expence": Decimal("5400.04"),
            "balance": Decimal("3899.99"),
        }
        self.assertDictEqual(balance, d)

    def test_balance_datelimit_wrong_date(self):
        balance = self.accounts["51"].getRemains(date(2021, 1, 17), date(2021, 1, 1))
        # pprint(balance)
        d = {
            "arrival": Decimal("0.00"),
            "expence": Decimal("0.00"),
            "balance": Decimal("0.00"),
        }
        self.assertDictEqual(balance, d)

    def test_balance_datelimit_zero_summ(self):
        balance = self.accounts["60"].getRemains(date(2021, 1, 16), date(2021, 1, 20))
        # pprint(balance)
        d = {
            "arrival": Decimal("0.00"),
            "expence": Decimal("0.00"),
            "balance": Decimal("0.00"),
        }
        self.assertDictEqual(balance, d)

    def test_balance_datelimit_enother_account(self):
        balance = self.accounts["62"].getRemains(date(2021, 1, 17), date(2021, 3, 11))
        # pprint(balance)
        d = {
            "arrival": Decimal("5600.06"),
            "expence": Decimal("7200.12"),
            "balance": Decimal("-1600.06"),
        }
        self.assertDictEqual(balance, d)


ENTRIES2 = [
    ("Test 1 1", date(2021, 1, 11), "51", "50", "-+", "1100.01", True),
    ("Test 2 1", date(2021, 1, 13), "50", "60", "--", "1200.02", True),
    ("Test 3 1", date(2021, 1, 15), "62", "60", "++", "1300.03", True),
    ("Test 4 1", date(2021, 1, 17), "62", "75", "--", "1400.04", True),
    ("Test 1 2", date(2021, 1, 19), "51", "50", "-+", "2100.01", True),
    ("Test 2 2", date(2021, 1, 21), "50", "60", "--", "2200.02", True),
    ("Test 3 2", date(2021, 1, 23), "62", "60", "++", "2300.03", False),
    ("Test 4 2", date(2021, 2, 10), "62", "75", "--", "2400.04", False),
    ("Test 1 3", date(2021, 2, 12), "51", "50", "-+", "3100.01", False),
    ("Test 2 3", date(2021, 2, 14), "50", "60", "--", "3200.02", False),
    ("Test 3 3", date(2021, 2, 16), "62", "60", "++", "3300.03", True),
    ("Test 4 3", date(2021, 2, 18), "62", "75", "--", "3400.04", True),
    ("Test 1 4", date(2021, 3, 11), "51", "50", "-+", "4100.01", True),
    ("Test 2 4", date(2021, 3, 13), "50", "60", "--", "4200.02", True),
    ("Test 3 4", date(2021, 3, 15), "62", "60", "++", "4300.03", True),
    ("Test 4 4", date(2021, 3, 17), "62", "75", "--", "4400.04", True),
]


class TestACard_Entries2(TestCase):
    def setUp(self) -> None:
        self.accounts = dict()
        for el in ACCOUNTS:
            self.accounts[str(el[0])] = Account.objects.create(
                number=el[0], name=el[1], fullName=el[2], is_active=el[3]
            )
        for el in ENTRIES2:
            Entry.objects.create(
                name=el[0],
                date=el[1],
                fAccount=self.accounts[el[2]],
                lAccount=self.accounts[el[3]],
                entryType=el[4],
                summ=el[5],
                is_enter=el[6],
            )

    def test_balance_datelimit_51(self):
        balance = self.accounts["51"].getRemains(date(2021, 1, 17), date(2021, 3, 11))
        # pprint(balance)
        d = {
            "arrival": Decimal("0.00"),
            "expence": Decimal("6200.02"),
            "balance": Decimal("-6200.02"),
        }
        self.assertDictEqual(balance, d)

    def test_balance_datelimit_75(self):
        balance = self.accounts["75"].getRemains(date(2021, 1, 17), date(2021, 3, 11))
        # pprint(balance)
        d = {
            "arrival": Decimal("0.00"),
            "expence": Decimal("4800.08"),
            "balance": Decimal("-4800.08"),
        }
        self.assertDictEqual(balance, d)

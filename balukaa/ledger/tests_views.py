from datetime import date
from decimal import Decimal
from pprint import pprint

from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import LedgerEntry, LedgerAccount
from registration.models import User


ACCOUNTS = [
    (50, 'Касса', 'Кассы', LedgerAccount.AccountTypes.ACTIVE),
    (51, 'РСчет', 'Расчетные счета', LedgerAccount.AccountTypes.ACTIVE),
    (60, 'Поставщики', 'Расчеты с поставщиками и подрядчиками', LedgerAccount.AccountTypes.VARIABLE),
    (41, 'Товары', 'Товары для продажи', LedgerAccount.AccountTypes.ACTIVE),
    (62, 'Покупатели', 'Расчеты с покупателями и заказчиками', LedgerAccount.AccountTypes.VARIABLE),
    (66, 'КЗаймы', 'Расчеты по краткосрочным кредитам и займам', LedgerAccount.AccountTypes.SOURCE),
    (67, 'ДЗаймы', 'Расчеты по долгосрочным кредитам и займам', LedgerAccount.AccountTypes.SOURCE),
]


ENTRIES = [
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


class TestACardView(TestCase):

    def setUp(self):
        self.accounts = dict()
        for el in ACCOUNTS:
            self.accounts[str(el[0])] = LedgerAccount.objects.create(
                number=el[0],
                name=el[1],
                full_name=el[2],
                type=el[3]
            )
        for el in ENTRIES:
            LedgerEntry.objects.create(
                date=el[0],
                account_one=self.accounts[el[1]],
                account_two=self.accounts[el[2]],
                type=el[3],
                amount=el[4],
                comment=el[5],
                status=el[6]
            )

        self.user = User.objects.create_user(username='user',
                                                   password='useer123456',
                                                   email='user@user.com')
        self.admin = User.objects.create_superuser(username='admin',
                                                         password='admin123456',
                                                         email='admin@user.com')


    def test_perms(self):
        response = self.client.get(f"/acard/{self.accounts['50'].id}")
        self.assertEqual(response.status_code, 302)

        self.client.login(username='user', password='user123456')

        response = self.client.get(f"/acard/{self.accounts['50'].id}")
        self.assertEqual(response.status_code, 302)

        self.client.logout()
        self.client.login(username='admin', password='admin123456')

        response = self.client.get(f"/acard/{self.accounts['50'].id}")
        self.assertEqual(response.status_code, 200)


    def test_context_without_params(self):
        self.client.login(username='admin', password='admin123456')
        response = self.client.get(f"/acard/{self.accounts['50'].id}")

        # print(type(response.context))
        # print('object_list size ', len(response.context['object_list']))
        # print(type(response.context['object_list'][0]))

        self.assertIn('object_list', response.context)
        self.assertEqual(len(response.context['object_list']), 6)
        self.assertIn('first', response.context)
        self.assertEqual(response.context['first'], date(2021, 1, 11))
        self.assertIn('last', response.context)
        self.assertEqual(response.context['last'], date(2021, 3, 17))
        self.assertIn('account', response.context)
        self.assertEqual(response.context['account'].number, 50)
        self.assertIn('opening_balance', response.context)
        self.assertDictEqual(response.context['opening_balance'],
                             {
            'arrival': Decimal('0.00'),
            'expense': Decimal('0.00'),
            'balance': Decimal('0.00'),
        })
        self.assertIn('final_balance', response.context)
        self.assertDictEqual(response.context['final_balance'],
                             {
            'arrival': Decimal('7300.03'),
            'expense': Decimal('7600.06'),
            'balance': Decimal('-300.03'),
        })


    def test_context_with_dates(self):
        self.client.login(username='admin', password='admin123456')
        response = self.client.get(f"/acard/{self.accounts['50'].id}", {'from': '20210117', 'to': '20210311'})

        self.assertIn('object_list', response.context)
        self.assertEqual(len(response.context['object_list']), 3)
        self.assertIn('first', response.context)
        self.assertEqual(response.context['first'], date(2021, 1, 17))
        self.assertIn('last', response.context)
        self.assertEqual(response.context['last'], date(2021, 3, 11))
        self.assertIn('account', response.context)
        self.assertEqual(response.context['account'].number, 50)
        self.assertIn('opening_balance', response.context)
        self.assertDictEqual(response.context['opening_balance'],
                             {
            'arrival': Decimal('1100.01'),
            'expense': Decimal('1200.02'),
            'balance': Decimal('-100.01'),
        })
        self.assertIn('final_balance', response.context)
        self.assertDictEqual(response.context['final_balance'],
                             {
            'arrival': Decimal('7300.03'),
            'expense': Decimal('3400.04'),
            'balance': Decimal('3899.99'),
        })

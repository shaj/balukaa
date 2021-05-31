from datetime import date
from decimal import Decimal
from pprint import pprint

from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import Entry, Account
from userapp.models import LedgerUser


ACCOUNTS = [
    (50, 'Касса', 'Касса', True),
    (51, 'Рсчет', 'Расчетный счет', True),
    (60, 'Поставщики', 'Расчеты с поставщиками и подрядчиками', False),
    (62, 'Товар', 'Товар', False),
    (75, 'Покупатели', 'Расчеты с покупателями', False),
]


ENTRIES = [
    ('Test 1 1', date(2021, 1, 11), '51', '50', 0, '1100.01', True),
    ('Test 2 1', date(2021, 1, 13), '50', '60', -1, '1200.02', True),
    ('Test 3 1', date(2021, 1, 15), '62', '60', 1, '1300.03', True),
    ('Test 4 1', date(2021, 1, 17), '62', '75', -1, '1400.04', True),
    ('Test 1 2', date(2021, 1, 19), '51', '50', 0, '2100.01', True),
    ('Test 2 2', date(2021, 1, 21), '50', '60', -1, '2200.02', True),
    ('Test 3 2', date(2021, 1, 23), '62', '60', 1, '2300.03', False),
    ('Test 4 2', date(2021, 2, 10), '62', '75', -1, '2400.04', False),
    ('Test 1 3', date(2021, 2, 12), '51', '50', 0, '3100.01', False),
    ('Test 2 3', date(2021, 2, 14), '50', '60', -1, '3200.02', False),
    ('Test 3 3', date(2021, 2, 16), '62', '60', 1, '3300.03', True),
    ('Test 4 3', date(2021, 2, 18), '62', '75', -1, '3400.04', True),
    ('Test 1 4', date(2021, 3, 11), '51', '50', 0, '4100.01', True),
    ('Test 2 4', date(2021, 3, 13), '50', '60', -1, '4200.02', True),
    ('Test 3 4', date(2021, 3, 15), '62', '60', 1, '4300.03', True),
    ('Test 4 4', date(2021, 3, 17), '62', '75', -1, '4400.04', True),
]


class TestACardView(TestCase):

    def setUp(self):

        self.accounts = dict()
        for el in ACCOUNTS:
            self.accounts[str(el[0])] = Account.objects.create(
                number=el[0],
                name=el[1],
                full_name=el[2],
                is_active=el[3]
            )
        for el in ENTRIES:
            Entry.objects.create(
                name=el[0],
                date=el[1],
                account_one=self.accounts[el[2]],
                account_two=self.accounts[el[3]],
                entry_type=el[4],
                sum=el[5],
                is_active=el[6]
            )

        self.user = LedgerUser.objects.create_user(username='user',
                                                   password='useer123456',
                                                   email='user@user.com')
        self.admin = LedgerUser.objects.create_superuser(username='admin',
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

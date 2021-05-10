from django.core.management.base import BaseCommand
from datetime import datetime, date
from django.utils import timezone
from ledger.models import Account, Entry


ACCOUNTS = [
    (50, 'Касса', 'Касса', True),
    (51, 'Рсчет', 'Расчетный счет', True),
    (60, 'Поставщики', 'Расчеты с поставщиками и подрядчиками', False),
    (62, 'Товар', 'Товар', False),
    (75, 'Покупатели', 'Расчеты с покупателями', False),
]


ENTRIES1 = [
    ('Test 1 1', date(2021, 1, 11), '51', '50', '-+', '1100.01', True),
    ('Test 2 1', date(2021, 1, 13), '50', '60', '--', '1200.02', False),
    ('Test 3 1', date(2021, 1, 15), '62', '60', '++', '1300.03', True),
    ('Test 4 1', date(2021, 1, 17), '62', '75', '--', '1400.04', True),
    ('Test 1 2', date(2021, 1, 19), '51', '50', '-+', '2100.01', True),
    ('Test 2 2', date(2021, 1, 21), '50', '60', '--', '2200.02', True),
    ('Test 3 2', date(2021, 1, 23), '62', '60', '++', '2300.03', False),
    ('Test 4 2', date(2021, 2, 10), '62', '75', '--', '2400.04', True),
    ('Test 1 3', date(2021, 2, 12), '51', '50', '-+', '3100.01', False),
    ('Test 2 3', date(2021, 2, 14), '50', '60', '--', '3200.02', True),
    ('Test 3 3', date(2021, 2, 16), '62', '60', '++', '3300.03', True),
    ('Test 4 3', date(2021, 2, 18), '62', '75', '--', '3400.04', False),
    ('Test 1 4', date(2021, 3, 11), '51', '50', '-+', '4100.01', True),
    ('Test 2 4', date(2021, 3, 13), '50', '60', '--', '4200.02', True),
    ('Test 3 4', date(2021, 3, 15), '62', '60', '++', '4300.03', True),
    ('Test 4 4', date(2021, 3, 17), '62', '75', '--', '4400.04', True),
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        # удаление всех объектов
        Entry.objects.all().delete()
        Account.objects.all().delete()

        # создание
        accounts = dict()
        for el in ACCOUNTS:
            accounts[str(el[0])] = Account.objects.create(
                number=el[0],
                name=el[1],
                fullName=el[2],
                is_active=el[3]
            )

        for el in ENTRIES1:
            Entry.objects.create(
                name=el[0],
                date=el[1],
                fAccount=accounts[el[2]],
                lAccount=accounts[el[3]],
                entryType=el[4],
                summ=el[5],
                is_enter=el[6]
            )


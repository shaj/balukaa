from datetime import date

from django.core.management.base import BaseCommand
from ledger.models import LedgerAccount, LedgerEntry

ACCOUNTS = [
    ('50', 'Касса', 'Кассы', LedgerAccount.AccountTypes.ACTIVE),
    ('51', 'РСчет', 'Расчетные счета', LedgerAccount.AccountTypes.ACTIVE),
    ('60', 'Поставщики', 'Расчеты с поставщиками и подрядчиками', LedgerAccount.AccountTypes.VARIABLE),
    ('41', 'Товары', 'Товары для продажи', LedgerAccount.AccountTypes.ACTIVE),
    ('62', 'Покупатели', 'Расчеты с покупателями и заказчиками', LedgerAccount.AccountTypes.VARIABLE),
    ('66', 'КЗаймы', 'Расчеты по краткосрочным кредитам и займам', LedgerAccount.AccountTypes.SOURCE),
    ('67', 'ДЗаймы', 'Расчеты по долгосрочным кредитам и займам', LedgerAccount.AccountTypes.SOURCE),
]

ENTRIES = [
    (date(2021, 1, 10), '51', '62', LedgerEntry.EntryTypes.RISE,
     '21000.00', 'Оплата от покупателя на рсчет', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 11), '51', '50', LedgerEntry.EntryTypes.MOVE,
     '4300.01', 'Снятие с рсчета в кассу', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 13), '50', '60', LedgerEntry.EntryTypes.FALL,
     '4300.01', 'Оплата из кассы поставщику', LedgerEntry.Statuses.DISABLE),
    (date(2021, 1, 15), '41', '60', LedgerEntry.EntryTypes.RISE,
     '4100.00', 'Поступление товара от поставщика', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 17), '41', '62', LedgerEntry.EntryTypes.FALL,
     '2900.77', 'Отгрузка товара покупателю', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 19), '51', '50', LedgerEntry.EntryTypes.MOVE,
     '3300.00', 'Снятие с рсчета в кассу', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 21), '50', '60', LedgerEntry.EntryTypes.FALL,
     '3200.02', 'Оплата из кассы поставщику', LedgerEntry.Statuses.ENABLE),
    (date(2021, 1, 23), '41', '60', LedgerEntry.EntryTypes.RISE,
     '3200.02', 'Поступление товара от поставщика', LedgerEntry.Statuses.DISABLE),
    (date(2021, 2, 10), '41', '62', LedgerEntry.EntryTypes.FALL,
     '3400.04', 'Отгрузка товара покупателю', LedgerEntry.Statuses.ENABLE),
    (date(2021, 2, 12), '51', '50', LedgerEntry.EntryTypes.MOVE,
     '2100.01', 'Снятие с рсчета в кассу', LedgerEntry.Statuses.DISABLE),
    (date(2021, 2, 14), '50', '60', LedgerEntry.EntryTypes.FALL,
     '2300.03', 'Оплата из кассы поставщику', LedgerEntry.Statuses.ENABLE),
    (date(2021, 2, 16), '41', '60', LedgerEntry.EntryTypes.RISE,
     '2300.03', 'Поступление товара от поставщика', LedgerEntry.Statuses.ENABLE),
    (date(2021, 2, 18), '41', '62', LedgerEntry.EntryTypes.FALL,
     '2300.03', 'Отгрузка товара покупателю', LedgerEntry.Statuses.DISABLE),
    (date(2021, 3, 11), '51', '50', LedgerEntry.EntryTypes.MOVE,
     '1100.01', 'Снятие с рсчета в кассу', LedgerEntry.Statuses.ENABLE),
    (date(2021, 3, 13), '50', '60', LedgerEntry.EntryTypes.FALL,
     '1100.01', 'Оплата из кассы поставщику', LedgerEntry.Statuses.ENABLE),
    (date(2021, 3, 15), '41', '60', LedgerEntry.EntryTypes.RISE,
     '900.12', 'Поступление товара от поставщика', LedgerEntry.Statuses.ENABLE),
    (date(2021, 3, 17), '41', '62', LedgerEntry.EntryTypes.FALL,
     '888.04', 'Отгрузка товара покупателю', LedgerEntry.Statuses.ENABLE),
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        # удаление всех объектов
        LedgerEntry.objects.all().delete()
        LedgerAccount.objects.all().delete()

        # создание
        accounts = dict()
        for account in ACCOUNTS:
            accounts[account[0]] = LedgerAccount.objects.create(
                number=account[0],
                name=account[1],
                full_name=account[2],
                type=account[3]
            )

        for entry in ENTRIES:
            LedgerEntry.objects.create(
                date=entry[0],
                account_one=accounts[entry[1]],
                account_two=accounts[entry[2]],
                type=entry[3],
                amount=entry[4],
                comment=entry[5],
                status=entry[6]
            )

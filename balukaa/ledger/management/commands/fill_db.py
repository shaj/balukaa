from django.core.management.base import BaseCommand
import datetime
from django.utils import timezone
from ledger.models import Account, Entry


class Command(BaseCommand):

    def handle(self, *args, **options):
        # удаление всех объектов
        Entry.objects.all().delete()
        Account.objects.all().delete()

        # создание
        account50 = Account.objects.create(number=50, name='Касса', fullName='Касса', is_active=True)
        account60 = Account.objects.create(number=60, name='Поставщики', 
                                           fullName='Расчеты с поставщиками и подрядчиками', 
                                           is_active=False
                                           )

        account70 = Account.objects.create(number=70, name='Товар', 
                                           fullName='Товар', 
                                           is_active=False
                                           )

        account80 = Account.objects.create(number=80, name='Покупатели', 
                                           fullName='Покупатели', 
                                           is_active=False
                                           )

        entry1 = Entry.objects.create(name='Снятие денег с рсч в кассу',
                                      date=datetime.date(2021, 1, 10),
                                      fAccount=account60,   # Поставщики
                                      lAccount=account50,   # Касса
                                      entryType=Entry.EntryType.MOVE.value,
                                      summ=1000.00,
                                      is_enter=False,
                                      created_at=timezone.now(),
                                      updates_at=timezone.now(),
                                      )

        entry2 = Entry.objects.create(name='Выплата поставщику',
                                      date=datetime.date(2021, 1, 11),
                                      fAccount=account50,   # Касса
                                      lAccount=account60,   # Поставщики
                                      entryType=Entry.EntryType.DECREASE.value,
                                      summ=500.00,
                                      is_enter=False,
                                      created_at=timezone.now(),
                                      updates_at=timezone.now(),
                                      )

        entry3 = Entry.objects.create(name='Приход товара',
                                      date=datetime.date(2021, 1, 12),
                                      fAccount=account70,   # Товар
                                      lAccount=account60,   # Поставщики
                                      entryType=Entry.EntryType.INCREASE.value,
                                      summ=1234.56,
                                      is_enter=False,
                                      created_at=timezone.now(),
                                      updates_at=timezone.now(),
                                      )

        entry3 = Entry.objects.create(name='Отгрузка товара',
                                      date=datetime.date(2021, 1, 13),
                                      fAccount=account70,   # Товар
                                      lAccount=account80,   # Покупатели
                                      entryType=Entry.EntryType.DECREASE.value,
                                      summ=7890.12,
                                      is_enter=True,
                                      created_at=timezone.now(),
                                      updates_at=timezone.now(),
                                      )


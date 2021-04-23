from django.core.management.base import BaseCommand
import datetime
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
                                      entryType='+-',
                                      summ=1000.00,
                                      is_enter=False,
                                      created_at=datetime.datetime.utcnow(),
                                      updates_at=datetime.datetime.utcnow(),
                                      )

        entry2 = Entry.objects.create(name='Выплата поставщику',
                                      date=datetime.date(2021, 1, 11),
                                      fAccount=account50,   # Касса
                                      lAccount=account60,   # Поставщики
                                      entryType='--',
                                      summ=500.00,
                                      is_enter=False,
                                      created_at=datetime.datetime.utcnow(),
                                      updates_at=datetime.datetime.utcnow(),
                                      )

        entry3 = Entry.objects.create(name='Приход товара',
                                      date=datetime.date(2021, 1, 12),
                                      fAccount=account70,   # Товар
                                      lAccount=account60,   # Поставщики
                                      entryType='++',
                                      summ=1234.56,
                                      is_enter=False,
                                      created_at=datetime.datetime.utcnow(),
                                      updates_at=datetime.datetime.utcnow(),
                                      )

        entry3 = Entry.objects.create(name='Отгрузка товара',
                                      date=datetime.date(2021, 1, 13),
                                      fAccount=account70,   # Товар
                                      lAccount=account80,   # Покупатели
                                      entryType='--',
                                      summ=7890.12,
                                      is_enter=True,
                                      created_at=datetime.datetime.utcnow(),
                                      updates_at=datetime.datetime.utcnow(),
                                      )

        # # 2. Несколько объектов по условию
        # # food = Food.objects.filter(<условие>)
        # # все бананы
        # food = Food.objects.filter(name='Банан')
        # print(food)
        # print(type(food))
        # food = Food.objects.filter(name='Жук')
        # print(food)

        # # Еда начинается со слова Ба
        # food = Food.objects.filter(name__startswith='Ба')

        # # Еда начинается со слова Ба и id < 1000
        # food = Food.objects.filter(name__startswith='Ба', id__lt=1000)
        # print(food)

        # # 3. 1 объект
        # food = Food.objects.get(name='Банан')
        # print(food.name)

        # # get or null
        # food = Food.objects.filter(name='jjj').first()
        # print(food)

        # food = Food.objects.filter(name='Банан')
        # food = food.filter(id__lt=1000)
        # food = food.filter(name__startswith='Ба')
        # print(food)

        # for _ in range(5):
        #     Animal.objects.create(name='Макс', kind=kind)
        #     Animal.objects.create(name='Михаил', kind=kind)
        print('end')


from django.core.management.base import BaseCommand
from animals.models import Family, Kind, Animal, Food


class Command(BaseCommand):

    def handle(self, *args, **options):
        # удаление всех объектов
        Food.objects.all().delete()
        Family.objects.all().delete()
        Kind.objects.all().delete()
        # создавать
        family = Family.objects.create(name='Медведь')
        print(family.id)

        # создание связанных объектов
        # FK
        kind = Kind.objects.create(name='Бурый', family=family)
        print(kind.id)

        banana = Food.objects.create(name='Банан')
        honey = Food.objects.create(name='Мед')
        # ManyToMany
        kind.food.add(banana)
        kind.food.add(honey)
        kind.save()

        print(kind.food.all())

        # Иземенение
        family.name = 'Тигр'
        family.save()
        # удалить один объект
        # family.delete()
        print(family.name)
        # выбирать
        # 1. Все объекты
        food = Food.objects.all()
        for item in food:
            print(item)

        # 2. Несколько объектов по условию
        # food = Food.objects.filter(<условие>)
        # все бананы
        food = Food.objects.filter(name='Банан')
        print(food)
        print(type(food))
        food = Food.objects.filter(name='Жук')
        print(food)

        # Еда начинается со слова Ба
        food = Food.objects.filter(name__startswith='Ба')

        # Еда начинается со слова Ба и id < 1000
        food = Food.objects.filter(name__startswith='Ба', id__lt=1000)
        print(food)

        # 3. 1 объект
        food = Food.objects.get(name='Банан')
        print(food.name)

        # get or null
        food = Food.objects.filter(name='jjj').first()
        print(food)

        food = Food.objects.filter(name='Банан')
        food = food.filter(id__lt=1000)
        food = food.filter(name__startswith='Ба')
        print(food)

        for _ in range(5):
            Animal.objects.create(name='Макс', kind=kind)
            Animal.objects.create(name='Михаил', kind=kind)
        print('end')


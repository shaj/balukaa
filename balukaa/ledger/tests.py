from datetime import date
from django.test import TestCase
from django.utils import timezone
from .models import Account, Entry


# Create your tests here.
class TestAccounts(TestCase):

    def test_main(self):
        self.assertEqual(Account.objects.count(), 0)


class TestEntries(TestCase):

    def setUp(self):
        Account.objects.create(number=50, name='Касса',
                               fullName='Касса', is_active=True)
        Account.objects.create(number=60, name='Поставщики',
                               fullName='Расчеты с поставщиками и подрядчиками',
                               is_active=False
                               )
        Account.objects.create(number=70, name='Товар',
                               fullName='Товар',
                               is_active=False
                               )

        Account.objects.create(number=80, name='Покупатели',
                               fullName='Покупатели',
                               is_active=False
                               )

    def test_main_one(self):
        et = Entry.objects.create(name='Выплата поставщику',
                                  date=date(2021, 1, 11),
                                  fAccount=Account.objects.get(
                                      number=50),   # Касса
                                  lAccount=Account.objects.get(
                                      number=60),   # Поставщики
                                  entryType='--',
                                  summ=500.00,
                                  is_enter=False,
                                  created_at=timezone.now(),
                                  updates_at=timezone.now(),
                                  )
        self.assertEqual(Entry.objects.count(), 1)

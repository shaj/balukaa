from django.core.management.base import BaseCommand
from ledger.models import LedgerAccount, LedgerEntry


class Command(BaseCommand):

    def handle(self, *args, **options):

        entry3 = LedgerEntry.objects.all().first()

        print('id', entry3.id)
        print('type', entry3.type)

        print(entry3.amount)
        a = entry3.amount
        print(type(a), a)
        
        print(type(LedgerEntry.EntryTypes.MOVE), repr(LedgerEntry.EntryTypes.MOVE))
        print(type(LedgerEntry.EntryTypes['MOVE'].label), repr(LedgerEntry.EntryTypes['MOVE'].label))
        print(type(LedgerEntry.EntryTypes.MOVE.value), repr(LedgerEntry.EntryTypes.MOVE.value))

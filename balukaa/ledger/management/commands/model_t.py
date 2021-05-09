from django.core.management.base import BaseCommand
import datetime
from django.utils import timezone
from ledger.models import Account, Entry
from pprint import pprint


class Command(BaseCommand):

    def handle(self, *args, **options):

        entry3 = Entry.objects.all().first()

        print('id', entry3.id)
        print('entryType', entry3.entryType)

        print(entry3.summ)
        a = entry3.summ
        print(type(a), a)
        
        print(type(Entry.EntryType.MOVE), repr(Entry.EntryType.MOVE))
        print(type(Entry.EntryType['MOVE'].label), repr(Entry.EntryType['MOVE'].label))
        print(type(Entry.EntryType.MOVE.value), repr(Entry.EntryType.MOVE.value))

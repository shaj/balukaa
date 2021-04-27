from django.core.management.base import BaseCommand
import datetime
from django.utils import timezone
from ledger.models import Account, Entry


class Command(BaseCommand):

    def handle(self, *args, **options):

        entry3 = Entry.objects.all().first()

        print('id', entry3.id)
        print('entryType', entry3.entryType)
        # print('entryType', Entry.EntryType[entry3.entryType].name)
        print('entryType', Entry.EntryType['MOVE'].label)
        print('entryType', Entry.EntryType[entry3.entryType].value)



from django.core.management.base import BaseCommand
from ledger.models import LedgerEntry

from mixer.backend.django import mixer


class Command(BaseCommand):

    def handle(self, *args, **options):
        e = mixer.blend(LedgerEntry)
        print(e)

from django.core.management.base import BaseCommand
import datetime
from django.utils import timezone
from ledger.models import Account, Entry
from pprint import pprint

from mixer.backend.django import mixer


class Command(BaseCommand):
    def handle(self, *args, **options):
        e = mixer.blend(Entry)
        print(e)

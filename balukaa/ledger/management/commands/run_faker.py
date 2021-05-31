from django.core.management.base import BaseCommand
from pprint import pprint

from faker import Faker


class Command(BaseCommand):

    def handle(self, *args, **options):
        fake = Faker()
        print(fake.name())
        print(fake.text())
        print('========')
        print(fake.word())
        pprint(fake.color())
        print('END')

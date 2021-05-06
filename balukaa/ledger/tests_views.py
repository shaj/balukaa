from django.test import TestCase
from .models import Entry


class test_for_one(TestCase):
    
    def test_one(self):
        self.assertEqual(Entry.objects.count(), 0)
        
        
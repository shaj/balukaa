from django.contrib import admin
from .models import LedgerAccount, LedgerEntry


admin.site.register(LedgerAccount)
admin.site.register(LedgerEntry)

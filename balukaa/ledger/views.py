from django.shortcuts import render
from .models import Account, Entry

# Create your views here.
def main(request):
    # tasks = Task.objects.order_by('-id')
    entries = Entry.objects.all().order_by('id')
    return render(request, 'ledger/index.html',
                  {
                      'entries': entries,
                  })


def account(request):
    accounts = Account.objects.all().order_by("number")
    return render(request, 'ledger/account.html',
                  {
                      'accounts': accounts,
                  })


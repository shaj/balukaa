import decimal
from typing import Any, Dict
from datetime import date, datetime
from dataclasses import dataclass
from decimal import Decimal
from pprint import pprint

from django.db.models.query import QuerySet
from django.db.models import Q
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Account, Entry
from .forms import EntryForm


class AboutView(TemplateView):
    template_name = 'ledger/about.html'


class EntriesListView(ListView):
    model = Entry
    template_name = 'ledger/index.html'
    
    
class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = 'ledger/entry_det.html'


class EntryCreateView(UserPassesTestMixin, CreateView):
    model = Entry
    template_name = 'ledger/entry_edit.html'
    form_class = EntryForm
    success_url = '/'

    def test_func(self):
        # return super().test_func()
        return self.request.user.is_superuser

    # def post(self, request, *args, **kwargs):
    #     print(request.user)
    #     return super().post(request, args, kwargs)

    # def form_valid(self, form):
    #     print('Form validating')
    #     return super().form_valid(form)

    
class EntryEditView(UpdateView):
    model = Entry
    template_name = 'ledger/entry_edit.html'
    form_class = EntryForm
    success_url = '/'


class AccountsListView(ListView):
    model = Account
    template_name = 'ledger/account.html'
    
    def get_queryset(self):
        return Account.objects.all().order_by("number")


class MoviListView(ListView):
    template_name = 'ledger/move.html'
    
    def get_queryset(self) -> QuerySet:
        queryset = Entry.objects.filter(is_enter=True).order_by("date")
        return queryset


@dataclass
class ACardRow:
    accDate: date
    corrAcc: str = ''
    arrival: Decimal = '0'
    expence: Decimal = '0'


class ACardView(TemplateView):
    template_name = 'ledger/acard.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # pprint(context)
        # pprint(kwargs)
        # pprint(self.kwargs)
        
        account = Account.objects.get(id=kwargs['pk'])
        # Здесь нужно найти минимальную дату в базе
        dateFrom = Entry.objects.earliest('date').date
        # Здесь нужно найти максимальную дату в базе
        dateTo = Entry.objects.latest('date').date

        try:
            dateFrom = datetime.strptime(self.request.GET.get('from'), '%Y%m%d')
        except Exception:
            pass
        try:
            dateTo = datetime.strptime(self.request.GET.get('to'), '%Y%m%d')
        except Exception:
            pass
        
        entries = Entry.objects \
            .filter(Q(lAccount=account.id) | Q(fAccount=account.id)) \
            .filter(is_enter=True) \
            .filter(date__gte=dateFrom) \
            .filter(date__lte=dateTo)
        
        object_list = []
        coming = Decimal('0.00')
        consumption = Decimal('0.00')
        balance = Decimal('0.00')
        for el in entries:
            row = ACardRow(el.date, None, '0', '0')
            if el.fAccount != account:
                row.corrAcc = el.fAccount.name
                if el.entryType == '-+':
                    row.arrival = el.summ
                    coming += el.summ
                elif el.entryType == '++':
                    row.arrival = el.summ
                    coming += el.summ
                else:
                    row.expence = el.summ
                    consumption += el.summ
            elif el.lAccount != account:
                row.corrAcc = el.lAccount.name
                if el.entryType == '-+':
                    row.expence = el.summ
                    consumption += el.summ
                elif el.entryType == '++':
                    row.arrival = el.summ
                    coming += el.summ
                else:
                    row.expence = el.summ
                    consumption += el.summ
            object_list.append(row)
        
        balance = coming - consumption
        
        context['object_list'] = object_list
        context['first'] = dateFrom
        context['last'] = dateTo
        context['account'] = account
        context['coming'] = coming
        context['consumption'] = consumption
        context['balance'] = balance
        
        return context
    
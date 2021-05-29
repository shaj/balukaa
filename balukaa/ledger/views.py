import decimal
from typing import Any, Dict
from datetime import date, datetime, timedelta
from dataclasses import dataclass
from decimal import Decimal
from pprint import pprint

from django.db.models.query import QuerySet
from django.db.models import Q
from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.urls import reverse_lazy
from .models import Account, Entry
from .forms import EntryForm


class AboutView(TemplateView):
    template_name = "ledger/about.html"


class EntriesListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = "ledger/index.html"


class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = "ledger/entry_det.html"


class EntryCreateView(PermissionRequiredMixin, CreateView):

    permission_required = "entry.add_choice"

    model = Entry
    template_name = "ledger/entry_edit.html"
    form_class = EntryForm
    success_url = reverse_lazy("ledger")


class EntryEditView(PermissionRequiredMixin, UpdateView):

    permission_required = "entry.change_choice"

    model = Entry
    template_name = "ledger/entry_edit.html"
    form_class = EntryForm
    success_url = reverse_lazy("ledger")


class AccountsListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = "ledger/account.html"

    def get_queryset(self):
        return Account.objects.all().order_by("number")


class MoviListView(LoginRequiredMixin, ListView):
    template_name = "ledger/move.html"

    def get_queryset(self) -> QuerySet:
        queryset = Entry.objects.filter(is_enter=True).order_by("date")
        return queryset


@dataclass
class ACardRow:
    accDate: date
    corrAcc: str = ""
    arrival: Decimal = "0"
    expence: Decimal = "0"


class ACardView(LoginRequiredMixin, TemplateView):
    template_name = "ledger/acard.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # pprint(context)
        # pprint(kwargs)
        # pprint(self.kwargs)

        account = Account.objects.get(id=kwargs["pk"])
        # Здесь нужно найти минимальную дату в базе
        dateEarliest = Entry.objects.earliest("date").date
        dateFrom = None
        dateTo = None

        try:
            dateFrom = datetime.strptime(self.request.GET.get("from"), "%Y%m%d").date()
        except Exception:
            dateFrom = dateEarliest
        try:
            dateTo = datetime.strptime(self.request.GET.get("to"), "%Y%m%d").date()
        except Exception:
            dateTo = Entry.objects.latest("date").date

        entries = Entry.objects.filter(
            Q(lAccount=account.id) | Q(fAccount=account.id),
            is_enter=True,
            date__gte=dateFrom,
            date__lte=dateTo,
        ).order_by("date")

        object_list = []
        for el in entries:
            row = ACardRow(el.date, None, "0", "0")
            if el.fAccount != account:
                row.corrAcc = el.fAccount.name
                if el.entryType == Entry.EntryType.MOVE.value:
                    row.arrival = el.summ
                elif el.entryType == Entry.EntryType.INCREASE.value:
                    row.arrival = el.summ
                else:
                    row.expence = el.summ
            elif el.lAccount != account:
                row.corrAcc = el.lAccount.name
                if el.entryType == Entry.EntryType.MOVE.value:
                    row.expence = el.summ
                elif el.entryType == Entry.EntryType.INCREASE.value:
                    row.arrival = el.summ
                else:
                    row.expence = el.summ
            object_list.append(row)

        context["object_list"] = object_list
        context["first"] = dateFrom
        context["last"] = dateTo
        context["account"] = account
        context["begin_balance"] = account.getRemains(
            dateEarliest, dateFrom - timedelta(days=1)
        )
        context["end_balance"] = account.getRemains(dateEarliest, dateTo)

        return context

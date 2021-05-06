from django.db.models.query import QuerySet
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Account, Entry
from .forms import EntryForm


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
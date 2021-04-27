from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from .models import Account, Entry
from .forms import EntryForm

# Create your views here.
# def main(request):
#     # tasks = Task.objects.order_by('-id')
#     entries = Entry.objects.all().order_by('id')
#     return render(request, 'ledger/index.html',
#                   {
#                       'entries': entries,
#                   })


class EntriesListView(ListView):
    model = Entry
    template_name = 'ledger/index.html'
    
    
class EntryDetailView(DetailView):
    model = Entry
    template_name = 'ledger/entry_det.html'


class EntryCreateView(CreateView):
    model = Entry
    template_name = 'ledger/entry_edit.html'
    form_class = EntryForm
    success_url = '/'

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

# def account(request):
#     accounts = Account.objects.all().order_by("number")
#     return render(request, 'ledger/account.html',
#                   {
#                       'accounts': accounts,
#                   })


class MoviListView(ListView):
    template_name = 'ledger/move.html'
    
    def get_queryset(self) -> QuerySet:
        queryset = Entry.objects.filter(is_enter=True).order_by("date")
        print(queryset)
        return queryset
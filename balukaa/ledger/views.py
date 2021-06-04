import decimal
from typing import Any, Dict
from datetime import date, datetime, timedelta
from dataclasses import dataclass

from django.db.models.query import QuerySet
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.formats import date_format
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import LedgerAccount, LedgerEntry
from .forms import LedgerEntryForm, LedgerAccountForm
from balukaa.nav_main_list import MENU


class AccountsBookListView(LoginRequiredMixin, ListView):
    model = LedgerAccount
    template_name = 'ledger/accounts_book.html'
    context_object_name = 'accounts'

    def get_context_data(self, **kwargs):
        """ Переменные шаблона

        title =     title сайта; заголовок navbar content
        btn_href =  ссылка для кнопки navbar content
        btn_text =  текст для кнопки navbar content
        cart_text = текст info-cart, вызываемой в случае отсутствия записей
        menu_list = список элементов dropdown меню: {item-group, item-text, item-url}
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'План счетов'
        context['btn_href'] = reverse_lazy('ledger:account_create')
        context['btn_text'] = 'Новый счет'
        context['cart_text'] = 'В плане счетов нет записей!'
        context['menu_list'] = MENU
        return context

    def get_queryset(self):
        return LedgerAccount.objects.all().order_by('number')


class AccountView(LoginRequiredMixin, DetailView):
    permission_required = 'account.view_choice'
    model = LedgerAccount
    template_name = 'ledger/account.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        """ Переменные шаблона

        title =     title сайта; заголовок navbar content
        btn_href =  ссылка для кнопки navbar content
        btn_text =  текст для кнопки navbar content
        menu_list = список элементов dropdown меню: {item-group, item-text, item-url}
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Бухгалтерский счет'
        context['btn_href'] = reverse_lazy('ledger:accounts_book')
        context['btn_text'] = 'План счетов'
        context['menu_list'] = MENU
        return context

    def get_object(self):
        """ Переопределяем стандартное получение объекта для DetailView по pk или slug на number

            Посмотрел здесь:
            https://stackru.com/questions/54206946/django-detailview-putanitsa-v-funktsii-getobject
        """
        return get_object_or_404(LedgerAccount, number=self.kwargs.get('number'))


class AccountCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'account.add_choice'
    model = LedgerAccount
    template_name = 'ledger/account_edit.html'   # account_create.html
    context_object_name = 'account'
    form_class = LedgerAccountForm

    def get_context_data(self, **kwargs):
        """ Переменные шаблона

        title =     title сайта; заголовок navbar content
        btn_href =  ссылка для кнопки navbar content
        btn_text =  текст для кнопки navbar content
        menu_list = список элементов dropdown меню: {item-group, item-text, item-url}
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f"Создать бухгалтерский счет"
        context['btn_href'] = reverse_lazy('ledger:accounts_book')
        context['btn_text'] = 'План счетов'
        context['menu_list'] = MENU
        return context


class AccountUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'account.change_choice'
    model = LedgerAccount
    template_name = 'ledger/account_edit.html'
    context_object_name = 'account'
    form_class = LedgerAccountForm

    def get_context_data(self, **kwargs):
        """ Переменные шаблона

        title =     title сайта; заголовок navbar content
        btn_href =  ссылка для кнопки navbar content
        btn_text =  текст для кнопки navbar content
        menu_list = список элементов dropdown меню: {item-group, item-text, item-url}
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f"Изменить бухгалтерский счет { self.kwargs.get('number') }"
        context['btn_href'] = reverse_lazy('ledger:accounts_book')
        context['btn_text'] = 'План счетов'
        context['menu_list'] = MENU
        return context

    def get_object(self):
        """ Переопределяем стандартное получение объекта для UpdateView по pk или slug на number

            Посмотрел здесь:
            https://stackru.com/questions/54206946/django-detailview-putanitsa-v-funktsii-getobject
        """
        return get_object_or_404(LedgerAccount, number=self.kwargs.get('number'))


class AccountDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'account.delete_choice'
    model = LedgerAccount
    template_name = 'ledger/account_delete.html'
    success_url = reverse_lazy('ledger:accounts_book')   # TODO: разобраться почему не работает reverse('ledger:accounts_book')
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        """ Переменные шаблона

        title =     title сайта; заголовок navbar content
        btn_href =  ссылка для кнопки navbar content
        btn_text =  текст для кнопки navbar content
        cart_text = текст info-cart, вызываемой в случае отсутствия записей
        menu_list = список элементов dropdown меню: {item-group, item-text, item-url}
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f"Удалить счет: {context['account'].number} {context['account'].name}"
        context['btn_href'] = reverse_lazy('ledger:accounts_book')
        context['btn_text'] = 'План счетов'
        context['cart_text'] = f"Счет: {context['account'].number} {context['account'].name}, " \
                               f"до удаления связанных с ним {context['account'].get_refs()} движений " \
                               f"в журнале проводок, удалить нельзя!"
        context['menu_list'] = MENU
        return context

    def get_object(self):
        """ Переопределяем стандартное получение объекта для DetailView по pk или slug на number

            Посмотрел здесь:
            https://stackru.com/questions/54206946/django-detailview-putanitsa-v-funktsii-getobject
        """
        return get_object_or_404(LedgerAccount, number=self.kwargs.get('number'))


class EntriesJournalListView(LoginRequiredMixin, ListView):
    model = LedgerEntry
    template_name = 'ledger/entries_journal.html'
    context_object_name = 'entries'

    def get_context_data(self, **kwargs):
        """ Переменные шаблона

        title =     title сайта; заголовок navbar content
        btn_href =  ссылка для кнопки navbar content
        btn_text =  текст для кнопки navbar content
        cart_text = текст info-cart, вызываемой в случае отсутствия записей
        menu_list = список элементов dropdown меню: {item-group, item-text, item-url}
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Журнал проводок'
        context['btn_href'] = reverse_lazy('ledger:entry_create')
        context['btn_text'] = 'Новая проводка'
        context['cart_text'] = 'В журнале проводок нет записей!'
        context['menu_list'] = MENU
        return context


class EntryView(LoginRequiredMixin, DetailView):
    permission_required = 'entry.view_choice'
    model = LedgerEntry
    template_name = 'ledger/entry.html'
    context_object_name = 'entry'

    def get_context_data(self, **kwargs):
        """ Переменные шаблона

        title =     title сайта; заголовок navbar content
        btn_href =  ссылка для кнопки navbar content
        btn_text =  текст для кнопки navbar content
        menu_list = список элементов dropdown меню: {item-group, item-text, item-url}
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Проводка'
        context['btn_href'] = reverse_lazy('ledger:entries_journal')
        context['btn_text'] = 'Журнал проводок'
        context['menu_list'] = MENU
        return context


class EntryCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'entry.add_choice'
    model = LedgerEntry
    template_name = 'ledger/entry_edit.html'  # entry_create.html
    context_object_name = 'entry'
    form_class = LedgerEntryForm

    def get_context_data(self, **kwargs):
        """ Переменные шаблона

        title =     title сайта; заголовок navbar content
        btn_href =  ссылка для кнопки navbar content
        btn_text =  текст для кнопки navbar content
        menu_list = список элементов dropdown меню: {item-group, item-text, item-url}
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать проводку'
        context['btn_href'] = reverse_lazy('ledger:entries_journal')
        context['btn_text'] = 'Журнал проводок'
        context['menu_list'] = MENU
        return context


class EntryUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'entry.change_choice'
    model = LedgerEntry
    template_name = 'ledger/entry_edit.html'
    context_object_name = 'entry'
    form_class = LedgerEntryForm

    def get_context_data(self, **kwargs):
        """ Переменные шаблона

        title =     title сайта; заголовок navbar content
        btn_href =  ссылка для кнопки navbar content
        btn_text =  текст для кнопки navbar content
        menu_list = список элементов dropdown меню: {item-group, item-text, item-url}
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f"Изменить проводку id={ self.kwargs.get('pk') }"
        context['btn_href'] = reverse_lazy('ledger:entries_journal')
        context['btn_text'] = 'Журнал проводок'
        context['menu_list'] = MENU
        return context


class EntryDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'entry.delete_choice'
    model = LedgerEntry
    template_name = 'ledger/entry_delete.html'
    success_url = reverse_lazy('ledger:entries_journal') # TODO: разобраться почему не работает reverse('ledger:entries_journal')
    context_object_name = 'entry'
    # form_class = LedgerEntryForm

    def get_context_data(self, **kwargs):
        """ Переменные шаблона

        title =     title сайта; заголовок navbar content
        btn_href =  ссылка для кнопки navbar content
        btn_text =  текст для кнопки navbar content
        menu_list = список элементов dropdown меню: {item-group, item-text, item-url}
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f"Удалить проводку id={ self.kwargs.get('pk') }"
        context['btn_href'] = reverse_lazy('ledger:entries_journal')
        context['btn_text'] = 'Журнал проводок'
        context['menu_list'] = MENU
        return context


class MovementsReportListView(LoginRequiredMixin, ListView):
    template_name = 'ledger/movements_report.html'
    context_object_name = 'entries'

    def get_context_data(self, **kwargs):
        """ Переменные шаблона

        title =     title сайта; заголовок navbar content
        btn_href =  ссылка для кнопки navbar content
        btn_text =  текст для кнопки navbar content
        cart_text = текст info-cart, вызываемой в случае отсутствия записей
        menu_list = список элементов dropdown меню: {item-group, item-text, item-url}
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Движения по журналу проводок'
        context['btn_href'] = reverse_lazy('ledger:entries_journal')
        context['btn_text'] = 'Журнал проводок'
        context['cart_text'] = 'В журнале проводок нет движений!'
        context['menu_list'] = MENU
        return context

    def get_queryset(self) -> QuerySet:
        queryset = LedgerEntry.objects.filter(
                       status=LedgerEntry.Statuses.ENABLE
                   ).order_by("date")
        return queryset


@dataclass
class AccountCardReportRow:
    account_date: date
    correspondent_account_number: str = ''
    correspondent_account_name: str = ''
    arrival: decimal.Decimal = '0'
    expense: decimal.Decimal = '0'
    current_balance: decimal.Decimal = '0'


class AccountCardReportView(LoginRequiredMixin, TemplateView):
    template_name = 'ledger/account_card_report.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """ Переменные шаблона

        account_cart_rows =       строка карточки
        date_from =               дата начала периода расчета карточки
        date_to =                 дата конца периода расчета карточки
        account =                 счет по которому расчитывается карточка
        initial_state =           начальное сальдо
        turnover_for_the_period = обороты за период
        balance =                 конечное сальдо

        title =     title сайта; заголовок navbar content
        btn_href =  ссылка для кнопки navbar content
        btn_text =  текст для кнопки navbar content
        cart_text = текст info-cart, вызываемой в случае отсутствия записей
        menu_list = список элементов dropdown меню: {item-group, item-text, item-url}
        """
        context = super().get_context_data(**kwargs)

        account = LedgerAccount.objects.get(number=kwargs['number'])

        # Здесь нужно найти минимальную дату в базе
        date_earliest = LedgerEntry.objects.earliest('date').date
        date_from = None
        date_to = None

        try:
            date_from = datetime.strptime(self.request.GET.get('from'), '%Y%m%d').date()
        except Exception:
            date_from = date_earliest
        try:
            date_to = datetime.strptime(self.request.GET.get('to'), '%Y%m%d').date()
        except Exception:
            date_to = LedgerEntry.objects.latest('date').date
        
        initial_state = account.get_remains(date_earliest, date_from - timedelta(days=1))
        turnover_for_the_period = account.get_remains(date_from, date_to)

        entries = LedgerEntry.objects.filter(
                      Q(account_two=account.id) | Q(account_one=account.id),
                      status=LedgerEntry.Statuses.ENABLE,
                      date__gte=date_from,
                      date__lte=date_to
                  ).order_by('date')

        current_balance = initial_state['balance']
        account_cart_rows = []
        for entry in entries:
            row = AccountCardReportRow(entry.date)
            if entry.account_one != account:
                row.correspondent_account_number = str(entry.account_one.number)
                row.correspondent_account_name = entry.account_one.name
                if entry.type == LedgerEntry.EntryTypes.MOVE.value:
                    row.arrival = entry.amount
                elif entry.type == LedgerEntry.EntryTypes.RISE.value:
                    row.arrival = entry.amount
                else:
                    row.expense = entry.amount
            elif entry.account_two != account:
                row.correspondent_account_number = str(entry.account_two.number)
                row.correspondent_account_name = entry.account_two.name
                if entry.type == LedgerEntry.EntryTypes.MOVE.value:
                    row.expense = entry.amount
                elif entry.type == LedgerEntry.EntryTypes.RISE.value:
                    row.arrival = entry.amount
                else:
                    row.expense = entry.amount
            current_balance += decimal.Decimal(row.arrival) - decimal.Decimal(row.expense)
            row.current_balance = current_balance
            account_cart_rows.append(row)
               
        context['account_cart_rows'] = account_cart_rows
        context['date_from'] = date_from
        context['date_to'] = date_to
        context['account'] = account
        context['initial_state'] = initial_state
        context['turnover_for_the_period'] = turnover_for_the_period
        context['balance'] = initial_state['balance'] + turnover_for_the_period['balance']

        context['title'] = f'Карточка по счету: {account.number} {account.name} / ' \
                           f"Фильтр: от { date_format(date_from, 'SHORT_DATE_FORMAT') } " \
                           f"до { date_format(date_to, 'SHORT_DATE_FORMAT') }"
        context['btn_href'] = reverse_lazy('ledger:accounts_book')
        context['btn_text'] = 'План счетов'
        context['cart_text'] = f'В указанном периоде по счету: {account.number}\xa0{account.name}, - не было движений!'
        context['menu_list'] = MENU
        return context


@dataclass
class AccountBalanceReportRow:
    account_number: str = ''
    account_name: str = ''
    balance: decimal.Decimal = '0'


class AccountBalanceReportView(LoginRequiredMixin, TemplateView):
    """ Балансовый отчет на дату. Требует доработки !!!

    Надо:
    1) сделать выбор даты на которую делается баланс
    2) доработать Акт/Пас (изменчивые) счета -
        2.1) если сальдо '+', то отображать в Пассивах (это наш долг), иначе в Активах (это долг нам)
        2.2) в дальнейшем ту часть, например, Поставщиков, у которых сальдо '+', отображать в Пассивах,
        остальных в Активах (долги нам - это активы, которыми необходимо управлять)
    """
    template_name = 'ledger/account_balance_report.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """ Переменные шаблона

        active_accounts = активные счета для раздела Актива Баланса
        source_accounts = пассивные и изменчивые счета для раздела Пассива Баланса
        actives_balance = сальдо Активов
        sources_balance = сальдо Пассивов
        balance =         баланс Активов и Пассивов - должен быть 0

        title =     title сайта; заголовок navbar content
        btn_href =  ссылка для кнопки navbar content
        btn_text =  текст для кнопки navbar content
        menu_list = список элементов dropdown меню: {item-group, item-text, item-url}
        """
        context = super().get_context_data(**kwargs)

        date_report = datetime.now()    # В будущем сделать выбор даты !!!

        active_accounts = LedgerAccount.objects.filter(type=LedgerAccount.AccountTypes.ACTIVE)
        source_accounts = LedgerAccount.objects.filter(Q(type=LedgerAccount.AccountTypes.SOURCE) |
                                                       Q(type=LedgerAccount.AccountTypes.VARIABLE))

        actives_balance = decimal.Decimal()
        active_accounts_rows = []
        for account in active_accounts:
            row = AccountBalanceReportRow()
            row.account_number = account.number
            row.account_name = account.name
            row.balance = account.get_account_balance(date_report)
            active_accounts_rows.append(row)
            actives_balance += row.balance

        sources_balance = decimal.Decimal()
        source_accounts_rows = []
        for account in source_accounts:
            row = AccountBalanceReportRow()
            row.account_number = account.number
            row.account_name = account.name
            row.balance = account.get_account_balance(date_report)
            source_accounts_rows.append(row)
            sources_balance += row.balance

        context['active_accounts'] = active_accounts_rows
        context['source_accounts'] = source_accounts_rows
        context['actives_balance'] = actives_balance
        context['sources_balance'] = sources_balance
        context['balance'] = actives_balance - sources_balance

        context['title'] = f"Баланс на дату: {date_format(date_report, 'SHORT_DATE_FORMAT')}"
        context['btn_href'] = reverse_lazy('ledger:accounts_book')
        context['btn_text'] = 'План счетов'
        context['menu_list'] = MENU
        return context

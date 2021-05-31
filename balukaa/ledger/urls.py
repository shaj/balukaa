from django.urls import path
from .views import (
    AccountsBookListView, AccountView, AccountCreateView, AccountUpdateView, AccountDeleteView,
    EntriesJournalListView, EntryView, EntryCreateView, EntryUpdateView, EntryDeleteView,
    MovementsReportListView, AccountCardReportView, AccountBalanceReportView,
)


app_name = 'ledger'
urlpatterns = [
    path('accounts_book/', AccountsBookListView.as_view(), name='accounts_book'),
    path('account/<str:number>/', AccountView.as_view(), name='account_view'),
    path('account/create/', AccountCreateView.as_view(), name='account_create'),
    path('account/update/<str:number>/', AccountUpdateView.as_view(), name='account_update'),
    path('account/delete/<str:number>/', AccountDeleteView.as_view(), name='account_delete'),

    path('entries_journal', EntriesJournalListView.as_view(), name='entries_journal'),
    path('entry/<int:pk>/', EntryView.as_view(), name='entry_view'),
    path('entry/create/', EntryCreateView.as_view(), name='entry_create'),
    path('entry/update/<int:pk>/', EntryUpdateView.as_view(), name='entry_update'),
    path('entry/delete/<int:pk>/', EntryDeleteView.as_view(), name='entry_delete'),

    path('movements_report/', MovementsReportListView.as_view(), name='movements_report'),
    path('account_card_report/<str:number>', AccountCardReportView.as_view(), name='account_card_report'),
    path('account_balance_report/', AccountBalanceReportView.as_view(), name='account_balance_report'),
]

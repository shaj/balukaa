
from django.urls import path
from .views import (
    EntriesListView, 
    EntryDetailView,
    EntryCreateView,
    EntryEditView,

    AccountsListView, 
    MoviListView, 
)


urlpatterns = [
    path('', EntriesListView.as_view(), name='ledger'),
    path('entry/<int:pk>/', EntryDetailView.as_view()),
    path('entry/new/', EntryCreateView.as_view(), name='ledger_new'),
    path('entry/edit/<int:pk>/', EntryEditView.as_view()),

    path('account/', AccountsListView.as_view(), name='account'),
    path('move/', MoviListView.as_view(), name='move'),
]

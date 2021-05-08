
from django.urls import path
from .views import (
    AboutView,
    EntriesListView, 
    EntryDetailView,
    EntryCreateView,
    EntryEditView,

    AccountsListView, 
    MoviListView,
    ACardView,
)


urlpatterns = [
    path('', EntriesListView.as_view(), name='ledger'),
    path('about/', AboutView.as_view(), name='about'),
    path('entry/<int:pk>/', EntryDetailView.as_view(), name='entry_det'),
    path('entry/new/', EntryCreateView.as_view(), name='entry_new'),
    path('entry/edit/<int:pk>/', EntryEditView.as_view(), name='entry_edit'),

    path('account/', AccountsListView.as_view(), name='account'),
    
    path('move/', MoviListView.as_view(), name='move'),
    path('acard/<int:pk>', ACardView.as_view(), name='acard'),
]

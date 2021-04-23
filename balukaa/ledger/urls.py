
from django.urls import path
from .views import EntriesListView, AccountsListView, MoviListView

urlpatterns = [
    path('', EntriesListView.as_view(), name='main'),
    path('account/', AccountsListView.as_view(), name='account'),
    path('move/', MoviListView.as_view(), name='move'),
]

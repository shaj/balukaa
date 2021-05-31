from django.urls import path
from .views import (
    TodoJournalListView,
)


app_name = 'todo'
urlpatterns = [
    path('todos_journal', TodoJournalListView.as_view(), name='todos_journal'),
]

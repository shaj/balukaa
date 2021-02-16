
from django.urls import path
from . import views

urlpatterns = [
    path('ledger/account/', views.account, name='account'),
]

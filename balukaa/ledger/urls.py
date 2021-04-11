
from django.urls import path
from . import views

urlpatterns = [
    path('ledger/', views.main, name='main'),
    # path('ledger/account/', views.account, name='account'),
]

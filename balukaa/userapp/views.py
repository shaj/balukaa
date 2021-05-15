from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import LedgerUser
from .forms import NewUserForm

# Create your views here.
class NewUserView(CreateView):
    model = LedgerUser
    form_class = NewUserForm
    template_name = "userapp/newuser.html"
    success_url = "/"


class LedgerLoginView(LoginView):
    template_name = "userapp/login.html"

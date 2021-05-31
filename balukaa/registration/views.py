from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import User
from .forms import UserCreateForm, UserLoginForm


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'registration/register.html'
    extra_context = {'title': 'Зарегистрировать пользователя'}
    success_url = '/'


class UserLoginView(LoginView):
    model = User
    form_class = UserLoginForm
    template_name = 'registration/login.html'
    extra_context = {'title': 'Войти в систему'}
    success_url = '/'


class UserLogoutView(LogoutView):
    model = User
    success_url = '/'

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserModel, AuthenticationForm
from .models import User


class UserCreateForm(UserCreationForm):
    username = forms.CharField(
        max_length=64,
        label='Имя пользователя',
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
        )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'})
        )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'})
        )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')         # fields = '__all__'


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'password')

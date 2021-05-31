from datetime import date, datetime

from django import forms
from .models import LedgerAccount, LedgerEntry


class LedgerAccountForm(forms.ModelForm):
    number = forms.CharField(
        max_length=2,
        label='Номер счета',
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
        )
    name = forms.CharField(
        max_length=32,
        label='Краткое имя счета',
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
        )
    full_name = forms.CharField(
        max_length=64,
        label='Полное имя счета',
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
        )
    type = forms.ChoiceField(
        label='Тип счета',
        choices=LedgerAccount.AccountTypes.choices,
        widget=forms.Select(
            attrs={'class': 'form-control'})
        )

    class Meta:
        model = LedgerAccount
        fields = ('number', 'name', 'full_name', 'type')         # fields = '__all__'


class LedgerEntryForm(forms.ModelForm):
    ''' Для удобства в поле date надо установить виджет какого-нибудь DatePicker

    Например, попробовать bootstrap_datepicker_plus, отсюда:
    https://question-it.com/questions/289488/kak-ispolzovat-sredstvo-vybora-daty-v-prostoj-forme-django
    '''
    date = forms.DateTimeField(
        label='Дата проводки',
        widget=forms.DateInput(
            attrs={'class': 'form-control',
                   'type': 'datetime-local'
                   }),
        initial=datetime.today(),
        localize=True
        )
    account_one = forms.ModelChoiceField(
        label='Счет 1',
        queryset=LedgerAccount.objects.order_by('number'),
        empty_label="Выберите счет 1",
        widget=forms.Select(
            attrs={'class': 'form-control'})
        )
    account_two = forms.ModelChoiceField(
        label='Счет 2',
        queryset=LedgerAccount.objects.order_by('number'),
        empty_label="Выберите счет 2",
        widget=forms.Select(
            attrs={'class': 'form-control'})
        )
    type = forms.ChoiceField(
        label='Тип проводки',
        choices=LedgerEntry.EntryTypes.choices,
        widget=forms.Select(
            attrs={'class': 'form-control'})
        )
    amount = forms.DecimalField(
        label='Сумма',
        widget=forms.NumberInput(
            attrs={'class': 'form-control'})
        )
    comment = forms.CharField(
        max_length=256,
        label='Комментарий',
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'rows': 1})
        )
    status = forms.ChoiceField(
        label='Состояние проводки',
        choices=LedgerEntry.Statuses.choices,
        widget=forms.Select(
            attrs={'class': 'form-control'})
        )

    class Meta:
        model = LedgerEntry
        fields = ('date', 'account_one', 'account_two', 'type', 'amount', 'comment', 'status')

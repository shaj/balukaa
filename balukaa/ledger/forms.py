from django import forms
from .models import Entry, Account

# from django.forms import ModelForm, TextInput, Textarea


class MessageForm(forms.Form):
    theme = forms.CharField(
        label="Тема", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    text = forms.CharField(
        label="Текст", widget=forms.Textarea(attrs={"class": "form-control"})
    )


class EntryForm(forms.ModelForm):
    # model = Entry
    # fields = ['title', 'task']
    # widgets = {
    #     'title': forms.TextInput(attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Название'
    #         }),
    #     'task': forms.Textarea(attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Описание'
    #         })
    #     }

    class Meta:
        model = Entry
        fields = "__all__"

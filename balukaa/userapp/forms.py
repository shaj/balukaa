from django.contrib.auth.forms import UserCreationForm
from .models import LedgerUser


class NewUserForm(UserCreationForm):
    class Meta:
        model = LedgerUser
        # fields = '__all__'
        fields = ('username', 'email', 'password1', 'password2')
        
        
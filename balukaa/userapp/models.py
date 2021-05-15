from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class LedgerUser(AbstractUser):
    email = models.EmailField(unique=True)

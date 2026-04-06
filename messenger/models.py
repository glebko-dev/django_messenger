from django.db.models import EmailField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = EmailField(blank=True, null=True)
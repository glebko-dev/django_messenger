from django.db.models import Model, ManyToManyField, ForeignKey, EmailField, CASCADE
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = EmailField(blank=True, null=True)


class Chat(Model):
    users = ManyToManyField(User)


class Message(Model):
    sender = ForeignKey(User, on_delete=CASCADE)

    chat = ForeignKey(Chat, on_delete=CASCADE)

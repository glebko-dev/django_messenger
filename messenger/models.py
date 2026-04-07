from django.db.models import Model, ManyToManyField, CharField, ForeignKey, EmailField, CASCADE, SET_NULL
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    current_chat = ForeignKey('Chat', on_delete=SET_NULL, null=True, blank=True)

    email = EmailField(blank=True, null=True)


class Chat(Model):
    name = CharField(max_length=100, default='Чат')

    users = ManyToManyField('User')


class Message(Model):
    sender = ForeignKey(User, on_delete=CASCADE)

    text = CharField(max_length=1000, default='')

    chat = ForeignKey(Chat, on_delete=CASCADE)

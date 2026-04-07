from django.contrib import admin
from django.urls import path

from messenger.views import index, sign_in, sign_up, sign_out, create_new_chat, get_chat_messages, send_message


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', index, name='index'),
    path('sign_in', sign_in, name='sign_in'),
    path('sign_up', sign_up, name='sign_up'),
    path('sign_out', sign_out, name='sign_out'),
    path('create_new_chat', create_new_chat, name='create_new_chat'),
    path('get_chat_messages', get_chat_messages, name='get_chat_messages'),
    path('send_message', send_message, name='send_message'),
]

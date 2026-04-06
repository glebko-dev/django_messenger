from django.contrib import admin
from django.urls import path

from messenger.views import index, sign_in, sign_up, sign_out


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', index, name='index'),
    path('sign_in', sign_in, name='sign_in'),
    path('sign_up', sign_up, name='sign_up'),
    path('sign_out', sign_out, name='sign_out'),
]

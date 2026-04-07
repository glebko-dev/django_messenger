from django.contrib import admin

from messenger.models import User, Chat, Message


admin.site.register(User)
admin.site.register(Chat)
admin.site.register(Message)

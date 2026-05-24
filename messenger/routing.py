from django.urls import path
from messenger.consumers import ChatConsumer, NewChatConsumer


websocket_urlpatterns = [
    path('ws/chat/<int:chat_id>/', ChatConsumer.as_asgi()),
    path('ws/chats/', NewChatConsumer.as_asgi()),
]

from channels.generic.websocket import AsyncWebsocketConsumer

from json import dumps

from asgiref.sync import sync_to_async

from messenger.models import Message, Chat

from channels.db import database_sync_to_async


@database_sync_to_async
def get_chat_messages(chat_id):
    chat = Chat.objects.filter(id=chat_id).first()

    messages = Message.objects.filter(chat=chat).prefetch_related('media')

    messages_list = []

    for message in messages:
        media = {msg.id: msg.file.name for msg in message.media.all() if msg.file}

        messages_list.append({
            'id': message.id,
            'sender__username': message.sender.username if message.sender else None,
            'text': message.text,
            'media': media if media else None
        })

    return messages_list


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']

        self.room_group_name = f'{self.chat_id}_chat_group'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def chat_message(self, event):
        messages_list = await get_chat_messages(self.chat_id)

        await self.send(text_data=dumps({
            'messages': messages_list
        }))


class NewChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        self.room_group_name = f'{self.user.username}_new_chat_group'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def new_chat_message(self, event):
        chats = Chat.objects.filter(users=self.user)

        chats_list = await sync_to_async(list)(
            chats.values('name', 'id')
        )

        await self.send(text_data=dumps({
            'chats': chats_list
        }))

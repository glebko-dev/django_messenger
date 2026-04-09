from channels.generic.websocket import AsyncWebsocketConsumer

from json import dumps

from asgiref.sync import sync_to_async

from messenger.models import Message, Chat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']

        self.room_group_name = f'{self.chat_id}_chat_group'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def chat_message(self, event):
        chat = await Chat.objects.filter(id=self.chat_id).afirst()

        messages = Message.objects.filter(chat=chat)

        messages_list = await sync_to_async(list)(
            messages.values('sender__username', 'text')
        )

        await self.send(text_data=dumps({
            'messages': messages_list
        }))

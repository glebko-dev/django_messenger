from channels.generic.websocket import AsyncWebsocketConsumer

from json import dumps

from asgiref.sync import sync_to_async

from messenger.models import Message, Chat, Media


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
        chat = await Chat.objects.filter(id=self.chat_id).afirst()

        messages = Message.objects.filter(chat=chat)

        messages_list = await sync_to_async(list)(
            messages.values('id', 'sender__username', 'text')
        )

        media_list = await sync_to_async(list)(
            messages.values('id', 'media__id')
        )

        for i in range(len(messages_list)):
            media_ids = []

            for j in range(len(media_list)):
                if media_list[j]['id'] == media_list[i]['id']:
                    media_ids.append(media_list[j]['media__id'])

            if media_ids == [None]:
                media_ids = []

            messages_list[i]['media'] = media_ids

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

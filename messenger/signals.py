from django.db.models.signals import post_save
from django.dispatch import receiver

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from messenger.models import Message


@receiver(post_save, sender=Message)
def message_notify(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()

        chat = instance.chat

        async_to_sync(channel_layer.group_send)(
            f'{chat.id}_chat_group',
            {
                'type': 'chat_message',
                'message': instance.text,
                'sender': instance.sender.username
            }
        )

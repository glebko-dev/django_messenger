from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from messenger.models import Message, Chat


@receiver(post_save, sender=Message)
def message_notify(sender, instance, created, **kwargs):
    if created and instance.media.exists() is False:
        channel_layer = get_channel_layer()

        chat = instance.chat

        async_to_sync(channel_layer.group_send)(
            f'{chat.id}_chat_group',
            {
                'type': 'chat_message'
            }
        )


@receiver(m2m_changed, sender=Message.media.through)
def message_media_notify(sender, instance, action, reverse, **kwargs):
    if action == 'post_add' and not reverse:
        channel_layer = get_channel_layer()

        chat = instance.chat

        async_to_sync(channel_layer.group_send)(
            f'{chat.id}_chat_group',
            {
                'type': 'chat_message'
            }
        )


@receiver(m2m_changed, sender=Chat.users.through)
def new_chat_notify(sender, instance, action, reverse, **kwargs):
    if action == 'post_add' and not reverse:
        channel_layer = get_channel_layer()

        for user in instance.users.all():
            async_to_sync(channel_layer.group_send)(
                f'{user.username}_new_chat_group',
                {
                    'type': 'new_chat_message',
                    'name': instance.name,
                    'id': instance.id
                }
            )

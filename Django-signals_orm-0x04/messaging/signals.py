from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification

import logging

logger = logging.getLogger(__name__)

# 1. Listen for Message post-save and create a Notification object
@receiver(post_save, sender=Message)
def create_notification_for_message(instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,  # assuming Message has a 'receiver' field
            message=instance
        )
        logger.info(f"Notification created for Message {instance.id}")

# 2. Listen for Notification post-save and simulate pushing (print notification data)
@receiver(post_save, sender=Notification)
def push_notification(instance, created, **kwargs):
    if created:
        notif_data = f"Push notification to {instance.user}: Message {instance.message.id}"
        print(notif_data)
        logger.info(notif_data)


#3. Listen for Message post-save and log the message content

# Log and store previous message content before edits
@receiver(pre_save, sender=Message)
def save_message_history(sender, instance, **kwargs):
    if not instance._state.adding:
        try:
            old_instance = Message.objects.get(pk=instance.pk)
            if old_instance.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_instance.content
                )
                instance.edited = True
                logger.info(f"Message {instance.pk} edited. Old content logged.")
        except Message.DoesNotExist:
            pass  # New message being created, skip history

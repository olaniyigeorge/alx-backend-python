from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

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

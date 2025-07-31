from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification, User

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


#3. Log and store previous message content before edits
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


# 4. Delete all related data when a user is deleted
@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    Deletes all messages, notifications, and message histories related to the user.
    This is triggered after a user account is deleted.
    """
    # Delete messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications received by the user
    Notification.objects.filter(recipient=instance).delete()

    # Delete message histories where user was editor
    MessageHistory.objects.filter(edited_by=instance).delete()

    logger.info(f"Cleaned up all related data for deleted user {instance.username}")
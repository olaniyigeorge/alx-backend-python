
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()




class Message(models.Model):
    message_id =  models.AutoField(primary_key=True, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    edited = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'message'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

        def __str__(self):
            return f"Message {self.message_id} from {self.sender} to {self.reciever}"
        

    def get_edit_history(self):
        """
        Return a list of previous versions of this message,
        showing who edited it and when.
        """
        return list(
            self.history.values('old_content', 'edited_at', 'edited_by__username').order_by('-edited_at')
        )
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'message_history'
        verbose_name = 'Message History'
        verbose_name_plural = 'Message Histories'



class Notification(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

        def __str__(self):
            return f"Notification for {self.recipient} regarding Message {self.message.message_id}"

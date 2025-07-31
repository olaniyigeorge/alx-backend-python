from django.contrib import admin
from .models import Message, MessageHistory, Notification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'receiver', 'content', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'content')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'message', 'read', 'created_at')
    list_filter = ('read',)
    search_fields = ('recipient__username', 'message__content')


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'old_content', 'edited_at')
    search_fields = ('old_content',)




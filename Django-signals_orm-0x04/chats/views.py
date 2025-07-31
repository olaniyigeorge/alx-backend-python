from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from messaging.models import Message

@cache_page(60)  
@login_required
def conversation_messages(request):
    """
    View that returns all messages between the logged-in user and another user.
    Cached for 60 seconds to improve performance.
    """
    other_user_id = request.GET.get("user_id")
    if not other_user_id:
        return JsonResponse({"error": "Missing user_id"}, status=400)

    messages = Message.objects.filter(
        sender_id__in=[request.user.id, other_user_id],
        reciever_id__in=[request.user.id, other_user_id]
    ).order_by("timestamp").only("content", "timestamp", "sender_id")

    data = [
        {
            "sender_id": msg.sender_id,
            "content": msg.content,
            "timestamp": msg.timestamp
        }
        for msg in messages
    ]

    return JsonResponse({"messages": data})

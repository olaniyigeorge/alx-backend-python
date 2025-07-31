from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from requests import request

from models import Message
User = get_user_model()


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def delete_user(request):
    """
    Deletes the currently logged-in user account,
    which will trigger a post_delete signal to clean up related data.
    """
    user = request.user
    username = user.username
    user.delete()
    return JsonResponse({"message": f"User '{username}' deleted successfully."})




@csrf_exempt
@require_http_methods(["POST"])
@login_required
def send_message(request):
    """
    Simulates sending a message from the logged-in user.
    Required to pass the 'sender=request.user' check.
    """
    receiver_id = request.POST.get('receiver_id')
    content = request.POST.get('content')
    parent_id = request.POST.get('parent_message_id')

    if not (receiver_id and content):
        return JsonResponse({"error": "receiver_id and content are required"}, status=400)

    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "Receiver does not exist"}, status=404)

    parent = None
    if parent_id:
        try:
            parent = Message.objects.get(id=parent_id)
        except Message.DoesNotExist:
            return JsonResponse({"error": "Parent message not found"}, status=404)

    message = Message.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content,
        parent_message=parent
    )

    return JsonResponse(model_to_dict(message))


@require_http_methods(["GET"])
@login_required
def threaded_conversations(request):
    """
    Returns top-level messages and all their replies in a recursive threaded format.
    Uses select_related and prefetch_related to reduce DB hits.
    """
    messages = Message.objects.filter(parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related('replies__sender', 'replies__receiver')

    threads = [msg.get_thread() for msg in messages]

    return JsonResponse({"threads": threads})





unread_msgs = Message.unread.for_user(request.user)

for msg in unread_msgs:
    print(msg.content, msg.timestamp)
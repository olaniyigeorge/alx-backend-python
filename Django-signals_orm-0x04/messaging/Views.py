from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

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

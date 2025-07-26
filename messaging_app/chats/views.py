from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets

from chats.models import User

# Create your views here.





def index(request): 
    """
    Render the index page for the chat application.
    """   
    return HttpResponse("<h1>Welcome to the Chat Application!</h1>")


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for handling user-related operations.
    """

    def list(self, request):
        """
        List all chats.
        """
        users = User.objects.all()

        return JsonResponse(
            {
                "message": "List of users",
                "data": users })

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific chat by its ID.
        """
        user = User.objects.get(pk=pk)
        return JsonResponse(
            {
                "message": f"User {user.username} details",
                "data": user
            }
        )
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.





def index(request): 
    """
    Render the index page for the chat application.
    """   
    return HttpResponse("<h1>Welcome to the Chat Application!</h1>")
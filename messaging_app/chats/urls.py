






from django.urls import path
from .views import index


urlpatterns = [
    path('', index, name='index'),
    path('conversations/', index, name='conversations'),
    path('conversations/<int:conversation_id>/', index, name='conversation_detail'),
    path('messages/', index, name='list_messages'),
    path('send_message/', index, name='send_message'),
    path('users/', index, name='list_create_users'),
]
from django.urls import path, include
from rest_framework import routers
from chats.views import index, UserViewSet, ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', index, name='index'),
    path('', include(router.urls)),  
]

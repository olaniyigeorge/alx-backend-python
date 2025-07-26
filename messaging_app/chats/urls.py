from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chats.views import index, UserViewSet, ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', index, name='index'),
    path('', include(router.urls)),  
]

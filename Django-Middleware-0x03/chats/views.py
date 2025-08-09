from django.http import HttpResponse
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


from chats.models import User, Conversation, Message
from chats.serializers import (
    UserCreateSerializer,
    UserSerializer, 
    ConversationSerializer, 
    MessageSerializer
)


from chats.permissions import IsParticipantOfConversation
from chats.filters import MessageFilter
from chats.pagination import MessagePagination


def index(request): 
    """
    Render the index page for the chat application.
    """   
    return HttpResponse("<h1>Welcome to the Chat Application!</h1>")


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for handling user-related operations.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['role']
    search_fields = ['email', 'username', 'first_name', 'last_name']


    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"message": "List of users", "data": serializer.data})

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # This will call create_user() and hash the password
            output_serializer = UserSerializer(user)
            return Response({
                "message": "User created successfully",
                "data": output_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConversationViewSet(viewsets.ViewSet):
    """
    ViewSet for listing and creating conversations.
    """

    def list(self, request):
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response({"message": "List of conversations", "data": serializer.data})

    def create(self, request):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            conversation = serializer.save()
            print(f"Conversation created: {conversation}")
            return Response({"message": "Conversation created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ViewSet):
    """
    ViewSet for listing and sending messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['conversation', 'sender']
    search_fields = ['content']

    def list(self, request, conversation_pk=None):
        """
        Optionally filter messages by conversation.
        """
        if conversation_pk:
            messages = Message.objects.filter(conversation_id=conversation_pk)
        else:
            messages = Message.objects.all()

        serializer = MessageSerializer(messages, many=True)
        return Response({"message": "List of messages", "data": serializer.data})

    def create(self, request, conversation_pk=None):
        """
        Send a new message in a specific conversation.
        """
        data = request.data.copy()
        if conversation_pk:
            data['conversation'] = conversation_pk

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            message = serializer.save()
            return Response({
                "message": "Message sent",
                "data": MessageSerializer(message).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users can see users


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        # Limit to conversations the user participates in
        return Conversation.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ["content"]
    ordering_fields = ["timestamp"]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            return Response({"detail": "You are not a participant in this conversation."}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get("conversation")
        if self.request.user not in conversation.participants.all():
            return Response({"detail": "You cannot send messages in this conversation."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(sender=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            return Response({"detail": "You cannot update messages in this conversation."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            return Response({"detail": "You cannot delete messages in this conversation."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
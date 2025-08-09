from rest_framework import permissions

class IsParticipantOrOwner(permissions.BasePermission):
    """
    Custom permission to only allow users to access conversations or messages
    they are participants of.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # For Conversation objects
        if hasattr(obj, "participants"):
            return user in obj.participants.all()

        # For Message objects
        if hasattr(obj, "conversation"):
            return user in obj.conversation.participants.all()

        return False


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only authenticated participants in a conversation
    can send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # For Conversation objects
        if hasattr(obj, "participants"):
            return user in obj.participants.all()

        # For Message objects
        if hasattr(obj, "conversation"):
            return user in obj.conversation.participants.all()

        return False

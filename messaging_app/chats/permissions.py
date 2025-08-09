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
    Custom permission:
    - Only authenticated users can access
    - Only participants in a conversation can send, view, update, delete messages
    """

    def has_permission(self, request, view):
        # Must be authenticated for ANY action
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # If checking a Conversation object
        if hasattr(obj, "participants"):
            return user in obj.participants.all()

        # If checking a Message object, check via its conversation
        if hasattr(obj, "conversation"):
            return user in obj.conversation.participants.all()

        return False
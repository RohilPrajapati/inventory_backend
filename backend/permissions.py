from rest_framework import permissions
from users.tokens import decode_token


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to grant access only to admin users.
    """

    def has_permission(self, request, view):
        """Check if the user is authenticated and has an admin role."""
        if not request.user or not request.user.is_authenticated:
            return False

        payload = decode_token(request)
        return payload.get('role') == 'admin'

# staff ko permission 
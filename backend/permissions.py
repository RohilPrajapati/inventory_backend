from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role_id.role_id == 1 or request.user.role_id == 1:
            return True
        else:
            return False

# staff ko permission 
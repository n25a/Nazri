from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """allows view just to admin and developer"""

    def has_permission(self, request, view):
        user_role = request.user.role
        if user_role == 2 or user_role == 3:
            return True

        return False

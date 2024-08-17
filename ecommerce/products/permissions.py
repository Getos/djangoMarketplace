from rest_framework import permissions


class IsStaffUser(permissions.BasePermission):
    """
    Custom permission to only allow staff members to access the view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsStaffOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Allow access if user is a staff member or admin
        return request.user.is_staff or request.user.is_superuser

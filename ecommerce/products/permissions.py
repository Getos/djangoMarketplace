from rest_framework import permissions
# from rest_framework.permissions import BasePermission


# class IsStaffUser(permissions.BasePermission):
#     """
#     Custom permission to only allow staff members to access the view.
#     """

#     def has_permission(self, request, view):
#         return request.user and request.user.is_staff


# class IsStaffOrAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # Check if the user is authenticated
#         if not request.user or not request.user.is_authenticated:
#             return False

#         # Allow access if user is a staff member or admin
#         return request.user.is_staff or request.user.is_superuser


# class IsAdminUser(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             print(f"User: {request.user.username}")
#             print(f"Is Superuser: {request.user.is_superuser}")
#         return request.user and request.user.is_superuser
# from rest_framework import permissions


class isStaffEditorPermisson(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

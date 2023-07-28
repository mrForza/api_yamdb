from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            (request.user.is_authenticated and request.user.role == 'admin')
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'admin' or request.user.is_superuser
        )


class IsAuthorOrAdminOrModer(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'admin'
            or request.user.role == 'moderator'
            or obj.author == request.user
            or request.user.is_superuser
        )

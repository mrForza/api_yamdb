from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            obj.role == 'admin'
        )


class IsAuthorOrAdminOrModer(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            obj.role == 'admin'
            or obj.role == 'moderator'
            or obj.author == request.user
        )

from rest_framework import permissions


class CustomIsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    pass


class CustomIsAuthenticated(permissions.IsAuthenticated):
    pass


class CustomIsAdminUser(permissions.IsAdminUser):
    pass


class CustomUsers(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return True


class CustomAllowAny(permissions.AllowAny):
    def has_object_permission(self, request, view, obj):
        return True


class CustomAuthor(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)

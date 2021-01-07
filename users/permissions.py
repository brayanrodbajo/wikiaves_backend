from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS

from users.models import CustomUser


class AdminCustomPermission(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.role == 'A'
        )


class EditorCustomPermission(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        birds = CustomUser.objects.get(id=request.user.id).birds.all()
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.role == 'E' and
            any(bird.id == view.kwargs['pk'] for bird in birds)
        )

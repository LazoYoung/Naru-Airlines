from rest_framework import permissions

from .models import Pilot


class IsPilotOrReadOnly(permissions.BasePermission):
    message = "You are not allowed to perform this action."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        return Pilot.objects.filter(member=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True

        query = Pilot.objects.filter(member=request.user)

        if query.exists():
            return obj.pilot == query.get()

        return False

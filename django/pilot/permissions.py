from rest_framework import permissions

from .models import Pilot


class IsPilotOrReadOnly(permissions.BasePermission):
    message = "You are not allowed to perform this action."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True

        if not request.user.is_authenticated:
            return False

        return Pilot.objects.filter(member=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True

        if not request.user.is_authenticated:
            return False

        query = Pilot.objects.filter(member=request.user)

        if query.exists():
            return obj.pilot == query.get()

        return False


class IsPilot(permissions.BasePermission):
    message = "You are not allowed to perform this action."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return Pilot.objects.filter(member=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        query = Pilot.objects.filter(member=request.user)

        if query.exists():
            return obj.pilot == query.get()

        return False
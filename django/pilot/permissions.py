from rest_framework import permissions

from .models import Pilot


class IsPilot(permissions.BasePermission):
    message = "Only the pilots have access to this resource."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return Pilot.objects.filter(member=request.user).exists()

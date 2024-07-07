from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ObjectDoesNotExist

from .models import Member


class MemberBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        if email is None or password is None:
            return None

        try:
            member = Member.objects.get(email__iexact=email)
        except ObjectDoesNotExist:
            return None

        if not member.check_password(password):
            return None

        if not member.is_active:
            return None

        return member

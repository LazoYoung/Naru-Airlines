import random
import string

from allauth.account.utils import setup_user_email
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from .models import Member
from rest_framework.serializers import HyperlinkedModelSerializer, as_serializer_error
from django.core.exceptions import ValidationError as DjangoValidationError
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress


class MemberSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = ['url', 'handle', 'display_name', 'email']


class MemberRegisterSerializer(RegisterSerializer):
    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if email and EmailAddress.objects.filter(email__iexact=email).exists():
            raise ValidationError("This e-mail is already in use.")
        return email

    def get_unique_handle(self):
        handle = "user-" + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        if get_user_model().objects.filter(handle=handle).exists():
            return self.get_unique_handle()
        return handle

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise ValidationError(
                    detail=as_serializer_error(exc)
                )
        user.handle = self.get_unique_handle()
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user

import random
import re
import string

from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError

from .models import Member

regex_email = re.compile(r"^[\w\-.]+@([\w-]+\.)+[\w-]{2,4}$")
regex_password_alphabet = re.compile(r"[a-zA-Z]+")
regex_password_whitespace = re.compile(r"\s+")
regex_password_special = re.compile(r"[0-9~!@#$%^&*()\-=_;:\',.?<>]+")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = self.get_user(email=email, password=password)
        else:
            raise ValidationError("Email or password is empty.")

        if not user:
            raise ValidationError("Email or password is wrong.")

        if not user.is_active:
            raise ValidationError("Your account is suspended.")

        if not user.is_verified:
            raise ValidationError("E-mail is not verified.")

        attrs['user'] = user
        return attrs

    @staticmethod
    def get_user(email, password):
        return authenticate(email=email, password=password)


class RegisterSerializer(serializers.Serializer):
    display_name = serializers.CharField(max_length=32)
    email = serializers.EmailField(max_length=32)
    password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_display_name(display_name):
        if len(display_name) < 2:
            raise ValidationError("Name is too short.")
        if len(display_name) > 32:
            raise ValidationError("Name is too long.")
        return display_name

    @staticmethod
    def validate_email(email):
        email = email.lower()
        if not regex_email.match(email):
            raise ValidationError("E-mail is invalid.")
        if Member.objects.filter(email=email).exists():
            raise ValidationError("E-mail is already in use.")
        return email

    @staticmethod
    def validate_password(password):
        validate_password(password)
        return password

    def save(self, request):
        user = Member.objects.create_user(
            handle=self.get_unique_handle(),
            display_name=self.validated_data['display_name'],
            email=self.validated_data['email'],
            password=self.validated_data['password'],
        )
        return user

    def get_unique_handle(self):
        handle = "user-" + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        if Member.objects.filter(handle=handle).exists():
            return self.get_unique_handle()
        return handle


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, old_password):
        request: Request = self.context['request']

        if request.user is AnonymousUser:
            raise ValidationError("You must log in first.")

        if not request.user.check_password(old_password):
            raise ValidationError("Incorrect password.")

        return old_password

    @staticmethod
    def validate_new_password(new_password):
        validate_password(new_password)
        return new_password

    def save(self, request: Request):
        member = request.user
        member.set_password(self.validated_data['new_password'])


def validate_password(password):
    if len(password) < 6:
        raise ValidationError("Password is too short.")
    if len(password) > 32:
        raise ValidationError("Password is too long.")
    if regex_password_whitespace.search(password):
        raise ValidationError("No whitespace allowed.")
    if not regex_password_alphabet.search(password):
        raise ValidationError("At least 1 alphabet is required.")
    if not regex_password_special.search(password):
        raise ValidationError("At least 1 digit or special character is required.")
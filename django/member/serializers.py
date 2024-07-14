import random
import re
import string

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

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

        if email is None:
            raise ValidationError({"email": "Email is required"})

        if password is None:
            raise ValidationError({"password": "Password is required"})

        user = self.get_user(email=email, password=password)

        if user is None:
            raise ValidationError("Wrong email or password.")

        if not user.is_active:
            raise ValidationError("Account is suspended.")

        if not user.is_verified:
            raise ValidationError("E-mail not verified.")

        attrs['user'] = user
        return attrs

    @staticmethod
    def get_user(email, password):
        return authenticate(email=email, password=password)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['display_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = Member.objects.create_user(
            handle=self.get_unique_handle(),
            display_name=validated_data['display_name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

    @staticmethod
    def validate_display_name(display_name):
        return validate_display_name(display_name)

    @staticmethod
    def validate_email(email):
        return validate_email(email)

    @staticmethod
    def validate_password(password):
        return validate_password(password)

    def get_unique_handle(self):
        handle = "user-" + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        if Member.objects.filter(handle=handle).exists():
            return self.get_unique_handle()
        return handle


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['receive_emails', 'display_name', 'bio', 'email', 'handle']
        extra_kwargs = {
            'handle': {'read_only': True},
            'email': {'read_only': True},
            'display_name': {'required': False},
        }

    def update(self, instance, validated_data):
        instance.receive_emails = validated_data.get('receive_emails', instance.receive_emails)
        instance.display_name = validated_data.get('display_name', instance.display_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={'input_type': 'password'}, required=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, required=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise ValidationError({"confirm_password": "Password does not match."})

        validate_password(new_password, "new_password")
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        request: Request = self.context['request']
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if not request.user.check_password(old_password):
            raise ValidationError({"old_password": "Incorrect password."})

        if new_password != confirm_password:
            raise ValidationError({"confirm_password": "Password does not match."})

        validate_password(new_password, "new_password")
        return attrs

    def save(self, request: Request):
        member = request.user
        member.set_password(self.validated_data['new_password'])
        member.save()


def validate_display_name(display_name):
    if len(display_name) < 2:
        raise ValidationError("Name is too short.")
    if len(display_name) > 32:
        raise ValidationError("Name is too long.")
    return display_name


def validate_email(email, key=None):
    if email is None:
        raise_validation_error("E-mail is required.", key)
    email = email.lower()
    if not regex_email.match(email):
        raise_validation_error("E-mail is invalid.", key)
    if Member.objects.filter(email=email).exists():
        raise_validation_error("E-mail is already in use.", key)
    return email


def validate_password(password, key=None):
    if len(password) < 6:
        raise_validation_error("Password is too short.", key)
    if len(password) > 32:
        raise_validation_error("Password is too long.", key)
    if regex_password_whitespace.search(password):
        raise_validation_error("No whitespace allowed.", key)
    if not regex_password_alphabet.search(password):
        raise_validation_error("At least 1 alphabet is required.", key)
    if not regex_password_special.search(password):
        raise_validation_error("At least 1 digit or special character is required.", key)
    return password


def raise_validation_error(error, key=None):
    if key is None:
        raise ValidationError(error)
    else:
        raise ValidationError({key: error})

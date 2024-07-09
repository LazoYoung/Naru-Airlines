from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Member, RegisterEmailToken
from .serializers import LoginSerializer, RegisterSerializer, PasswordChangeSerializer
from .tokens import account_activation_token
from .utils import get_random_password


@api_view(['POST'])
def login(request: Request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    django_login(request, user)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def logout(request: Request):
    django_logout(request)
    response = Response(
        data={'detail': _("Successfully logged out.")},
        status=status.HTTP_200_OK
    )
    return response


@api_view(['POST'])
def register(request: Request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(request)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
def send_register_email(request: Request):
    mail_address = request.data['email']

    try:
        member: Member = Member.objects.get(email__iexact=mail_address)
    except ObjectDoesNotExist:
        return Response(
            data="No account found with given e-mail.",
            status=status.HTTP_400_BAD_REQUEST
        )

    if member.is_verified:
        return Response(
            data="Account is already verified.",
            status=status.HTTP_400_BAD_REQUEST
        )

    token = account_activation_token.make_token(member)
    content = render_to_string(
        'auth/account_verification.html',
        context={
            'name': member.display_name,
            'scheme': request.scheme,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(member.pk)),
            'token': token,
        }
    )
    email = EmailMessage(
        subject="[Naru Airlines] Your account verification",
        body=content,
        to=[mail_address],
    )
    email.content_subtype = 'html'
    email.send()

    RegisterEmailToken.objects.create(
        member=member,
        token=token,
        valid_until=timezone.now() + timezone.timedelta(hours=1)
    )
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_register_email(uid: str, token: str):
    pk = urlsafe_base64_decode(uid)
    try:
        user: Member = Member.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(data="Account not found.", status=status.HTTP_400_BAD_REQUEST)

    if user.is_verified:
        return Response(data="Account is already verified.", status=status.HTTP_400_BAD_REQUEST)

    try:
        token: RegisterEmailToken = RegisterEmailToken.objects.get(token=token)
    except ObjectDoesNotExist:
        return Response(data="Token is invalid.", status=status.HTTP_400_BAD_REQUEST)

    if token.is_expired():
        return Response(data="Token is expired.", status=status.HTTP_400_BAD_REQUEST)

    user.is_verified = True
    user.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def change_password(request: Request):
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save(request)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def reset_password(request: Request):
    mail_address = request.data['email']
    try:
        member = Member.objects.get(email__iexact=mail_address)
        new_password = get_random_password()
        if member.is_active and member.is_verified:
            content = render_to_string(
                'auth/password_reset.html',
                context={
                    'name': member.display_name,
                    'new_password': new_password,
                }
            )
            email = EmailMessage(
                subject="[Naru Airlines] Your password reset",
                body=content,
                to=[mail_address],
            )
            email.content_subtype = 'html'
            email.send()
    except ObjectDoesNotExist:
        pass
    return Response(status=status.HTTP_200_OK)

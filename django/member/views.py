from typing import Optional

from django.conf import settings
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Member, AuthRequest
from .serializers import LoginSerializer, RegisterSerializer, ProfileSerializer, PasswordChangeSerializer
from .tokens import AuthTokenGenerator
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
    response = Response(status=status.HTTP_200_OK)
    return response


@api_view(['POST'])
def register(request: Request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT'])
def profile(request: Request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        serializer = ProfileSerializer(instance=request.user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class SendVerificationEmail(APIView):
    permission_classes = (IsAuthenticated,)
    member = None
    mail = None
    reason = None

    def post(self, request: Request):
        self.mail = request.data['email']

        try:
            self.member = Member.objects.get(email__iexact=self.mail)
        except ObjectDoesNotExist:
            return Response(
                data="No account found with given e-mail.",
                status=status.HTTP_400_BAD_REQUEST
            )

        return self.branch(request)

    def branch(self, request):
        try:
            reason = request.data['reason']
            if reason is None:
                return Response(
                    data=f"Missing form data: reason",
                    status=status.HTTP_400_BAD_REQUEST
                )
            self.reason = AuthRequest.Reason[reason.upper()]
        except KeyError:
            return Response(data="Bad form data: reason", status=status.HTTP_400_BAD_REQUEST)

        if self.reason == AuthRequest.Reason.REGISTER:
            return self.register(request)
        elif self.reason == AuthRequest.Reason.CHANGE_EMAIL:
            return self.change_email(request)

    def create_token(self):
        return AuthTokenGenerator().make_token(self.member)

    def get_content(self, request, token, template_name):
        content = render_to_string(
            template_name=template_name,
            context={
                'name': self.member.display_name,
                'scheme': request.scheme,
                'domain': get_current_site(request).domain,
                'uid': get_uid(self.member),
                'token': token,
            }
        )
        return content

    def register(self, request):
        if self.member.is_verified:
            return Response(
                data="Account is already verified.",
                status=status.HTTP_400_BAD_REQUEST
            )

        token = self.create_token()
        expiry_date = timezone.now() + timezone.timedelta(hours=1)
        mail = EmailMessage(
            subject="[Naru Airlines] Verify your new account.",
            body=self.get_content(request, token, 'auth/verify_account.html'),
            to=[self.mail],
        )
        mail.content_subtype = 'html'
        mail.send()
        AuthRequest.objects.create(
            reason=self.reason,
            member=self.member, token=token, valid_until=expiry_date
        )
        return Response(status=status.HTTP_200_OK)

    def change_email(self, request):
        if not self.member.is_verified:
            return Response(
                data="Account is not verified yet.",
                status=status.HTTP_400_BAD_REQUEST
            )

        new_email = request.data['new_email']

        if new_email is None:
            return Response(
                data="Missing form data: new_email",
                status=status.HTTP_400_BAD_REQUEST
            )

        token = self.create_token()
        expiry_date = timezone.now() + timezone.timedelta(hours=1)
        mail = EmailMessage(
            subject="[Naru Airlines] Confirm your new e-mail address.",
            body=self.get_content(request, token, 'auth/change_email.html'),
            to=[self.mail],
        )
        mail.content_subtype = 'html'
        mail.send()
        AuthRequest.objects.create(
            reason=self.reason, target=new_email.lower(),
            member=self.member, token=token, valid_until=expiry_date
        )
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def verify_register_email(_: Request, uid: str, token: str):
    try:
        user = get_user(uid)
    except ObjectDoesNotExist:
        return Response(data="Account not found.", status=status.HTTP_400_BAD_REQUEST)

    if user.is_verified:
        return Response(data="Account is already verified.", status=status.HTTP_400_BAD_REQUEST)

    try:
        auth_request = get_auth_request(token)
    except ObjectDoesNotExist:
        return Response(data="Token is invalid.", status=status.HTTP_400_BAD_REQUEST)

    if auth_request.is_expired():
        return Response(data="Token is expired.", status=status.HTTP_400_BAD_REQUEST)

    user.is_verified = True
    user.save()
    return redirect_login()


@api_view(['GET'])
def verify_change_email(_: Request, uid: str, token: str):
    try:
        user = get_user(uid)
    except ObjectDoesNotExist:
        return Response(data="Account not found.", status=status.HTTP_400_BAD_REQUEST)

    try:
        auth_request = get_auth_request(token)
    except ObjectDoesNotExist:
        return Response(data="Token is invalid.", status=status.HTTP_400_BAD_REQUEST)

    if auth_request.is_expired():
        return Response(data="Token is expired.", status=status.HTTP_400_BAD_REQUEST)

    user.set_password(auth_request.target)
    user.save()
    return redirect_login()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request: Request):
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save(request)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_password(request: Request):
    mail_address = request.data['email']
    try:
        member = Member.objects.get(email__iexact=mail_address)
        new_password = get_random_password()
        if member.is_active and member.is_verified:
            content = render_to_string(
                'auth/reset_password.html',
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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

    token = AuthTokenGenerator().make_token(member)
    content = render_to_string(
        'auth/verify_account.html',
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

    AuthRequest.objects.create(
        reason=AuthRequest.Reason.REGISTER,
        member=member,
        token=token,
        valid_until=timezone.now() + timezone.timedelta(hours=1)
    )
    return Response(status=status.HTTP_200_OK)


def get_user(uid: str) -> Member:
    pk = urlsafe_base64_decode(uid)
    return Member.objects.get(pk=pk)


def get_auth_request(token: str) -> AuthRequest:
    return AuthRequest.objects.get(reason=AuthRequest.Reason.REGISTER, token=token)


def redirect_login() -> Response:
    scheme = 'https' if settings.HTTPS else 'http'
    location = f'{scheme}://{Site.objects.get_current().domain}/login/'

    return Response(
        status=status.HTTP_301_MOVED_PERMANENTLY,
        headers={'Location': location}
    )


def get_uid(member: Member):
    return urlsafe_base64_encode(force_bytes(member.pk))

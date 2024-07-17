from django.db import models
from django.utils import timezone
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MemberManager(BaseUserManager):
    def create_user(self, handle, display_name, email, password=None):
        if not handle:
            raise ValueError("Users must have a handle")

        user = Member(handle=handle, display_name=display_name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, handle, display_name, email, password=None):
        superuser = self.create_user(handle=handle, display_name=display_name, email=email, password=password)
        superuser.is_admin = True
        superuser.save(using=self._db)
        return superuser


# noinspection PyMethodMayBeStatic
class Member(AbstractBaseUser):
    handleValidator = ASCIIUsernameValidator()
    handle = models.CharField(max_length=32, unique=True, validators=[handleValidator])
    display_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=128, unique=True)
    bio = models.TextField(max_length=256, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    receive_emails = models.BooleanField(default=True)

    objects = MemberManager()

    USERNAME_FIELD = 'handle'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['display_name', 'email']

    def __str__(self):
        return self.handle

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, abb_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class AuthRequest(models.Model):
    class Reason(models.IntegerChoices):
        REGISTER = 1
        CHANGE_EMAIL = 2
        RESET_PASSWORD = 3

    reason = models.CharField(choices=Reason.choices, max_length=32)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    target = models.CharField(max_length=64)
    valid_until = models.DateTimeField()

    objects = models.Manager()

    def __str__(self):
        return self.token

    def is_expired(self) -> bool:
        return timezone.now() >= self.valid_until

import datetime
import string
from secrets import choice

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from lib.models import BaseModel

DEFAULT_CODE_LENGTH = 6
DEFAULT_CODE_TTL_MINUTES = 60


class User(AbstractUser, BaseModel):
    code_last_sent = models.DateTimeField(blank=True, null=True)
    previous_emails = ArrayField(models.EmailField(), default=list)
    pending_new_email = models.EmailField(blank=True, null=True)
    pending_code = models.CharField(max_length=20, editable=False, blank=True, null=True)
    pending_code_timestamp = models.DateTimeField(editable=False, blank=True, null=True)

    def __str__(self):
        return f"{self.username}"

    @property
    def slug(self):
        return slugify(self.username)


class AuthCode(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="auth_codes", editable=False, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, editable=False)
    timestamp = models.DateTimeField(editable=False, auto_now=True)
    next_page = models.TextField(editable=False, default="/")

    def __str__(self):
        return f"{self.user.username} - {self.code}"

    @classmethod
    def send_auth_code(cls, user, code_uri, next_page=None):
        """Send an auth code to a user via email.

        Args:
          user: The user to whom the auth code should be sent.
          code_uri: The full URI for the code page.
          next_page: The page the user should be redirected to after login. (Default value = None)

        Returns:
          True if an auth code was created and sent to the user. False if a new auth code wasn't created
          (a previous code exists and was created within the TTL).
        """
        template = "log-in-email.txt"
        html_template = "log-in-email.html"

        auth_code = cls._create_code_for_user(user, next_page)
        if not auth_code:
            return False
        else:
            context = {
                "code": auth_code.code,
                "code_uri": code_uri,
                "email": auth_code.user.email,
                "site_name": settings.SITE_NAME,
            }

            subject, to = (_(f"Your {settings.SITE_NAME} log in code"), auth_code.user.email)
            msg = EmailMultiAlternatives(subject, render_to_string(template, context), None, [to])
            msg.attach_alternative(render_to_string(html_template, context), "text/html")
            msg.send()
            return True

    @classmethod
    def get_auth_code(cls, email, code):
        """Gets an auth code for a user, given an email address and code to verify.
        Will not return auth codes created outside of the NOAUTH_CODE_TTL_MINUTES window.

        Args:
          email: The email to use when looking up the auth code.
          code: The code to use when looking up the auth code.

        Returns:
          An auth code if one matching the parameters was found, otherwise None.

        """
        try:
            valid_timestamp_start = timezone.now() - datetime.timedelta(
                minutes=getattr(settings, "NOAUTH_CODE_TTL_MINUTES", DEFAULT_CODE_TTL_MINUTES)
            )
            return AuthCode.objects.get(user__username=email, code=code, timestamp__gte=valid_timestamp_start)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def _create_code_for_user(cls, user, next_page=None):
        """Creates an auth code for the given user.

        Args:
          user: The user that should be associated with the auth code.
          next_page: The page the user should be redirected to after authenticating (optional, defaults to /).

        Returns:
          The new auth code or None if the user is inactive (disabled) or an auth code has been created within the TTL window.

        """
        if not user.is_active:
            return None

        next_page = next_page or "/"
        next_page = next_page.replace("://", "")

        valid_timestamp_start = timezone.now() - datetime.timedelta(
            minutes=getattr(settings, "NOAUTH_CODE_TTL_MINUTES", DEFAULT_CODE_TTL_MINUTES)
        )
        if not AuthCode.objects.filter(user=user, timestamp__gte=valid_timestamp_start).exists():
            code = cls.generate_code()
            AuthCode.objects.filter(user=user).delete()
            return AuthCode.objects.create(user=user, code=code, next_page=next_page)
        else:
            return None

    @classmethod
    def generate_code(cls):
        code_length = getattr(settings, "NOAUTH_CODE_LENGTH", DEFAULT_CODE_LENGTH)
        return "".join(choice(string.digits) for i in range(code_length))

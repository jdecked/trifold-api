from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token

from .user_manager import UserManager


class User(AbstractBaseUser):
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'users'
        app_label = 'api'
    objects = UserManager()
    USERNAME_FIELD = 'email'

    # This is the user's Google ID, since emails can change.
    id = models.CharField(
        primary_key=True,
        editable=False,
        max_length=255,
        default=None
    )
    email = models.EmailField(unique=True)
    password = None
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)

    def get_email(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

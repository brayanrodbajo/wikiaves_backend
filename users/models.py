from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.db import models
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .authentication import is_token_expired

from birds.models import Author, Bird


class CustomUser(AbstractBaseUser, PermissionsMixin, Author):
    ROLE_CHOICES = [
        ('E', 'Editor'),
        ('A', 'Admin')
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField()
    role = models.CharField(max_length=6, choices=ROLE_CHOICES, default='E')
    birds = models.ManyToManyField(Bird, through='BirdCurrentEditor', related_name='current_editors')

    USERNAME_FIELD = 'username'
    objects = UserManager()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class BirdCurrentEditor(models.Model):
    bird = models.ForeignKey(Bird, related_name='bird_current_editors', null=True, on_delete=models.SET_NULL)
    editor = models.ForeignKey(CustomUser, related_name='current_editor_birds', null=True, on_delete=models.SET_NULL)


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')

        # Token Expiration
        if is_token_expired(token):
            raise AuthenticationFailed('Token has expired')

        return token.user, token

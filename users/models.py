from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.db import models

from birds.models import Bird, Author


class CustomUser(AbstractBaseUser, PermissionsMixin, Author):
    ROLE_CHOICES = [
        ('E', 'Editor'),
        ('A', 'Admin')
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField()
    role = models.CharField(max_length=6, choices=ROLE_CHOICES, default='E')
    birds = models.ManyToManyField(Bird, through='BirdEditor', related_name='editors')

    USERNAME_FIELD = 'username'
    objects = UserManager()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class BirdEditor(models.Model):
    bird = models.ForeignKey(Bird, related_name='bird_editor', null=True, on_delete=models.SET_NULL)
    editor = models.ForeignKey(CustomUser, related_name='editor_bird', null=True, on_delete=models.SET_NULL)

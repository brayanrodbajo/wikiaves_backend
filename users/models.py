from django.contrib.auth.models import AbstractUser
from django.db import models

from birds.models import Bird


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('E', 'Editor'),
        ('A', 'Admin')
    ]
    name = models.CharField(null=True, blank=True, max_length=255)
    role = models.CharField(max_length=6, choices=ROLE_CHOICES, default='E')
    birds = models.ManyToManyField(Bird, through='BirdEditor', related_name='editors')

    def __str__(self):
        return self.email


class BirdEditor(models.Model):
    bird = models.ForeignKey(Bird, related_name='bird_editor', null=True, on_delete=models.SET_NULL)
    editor = models.ForeignKey(CustomUser, related_name='editor_bird', null=True, on_delete=models.SET_NULL)

# Generated by Django 3.1 on 2021-07-16 11:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('birds', '0061_remove_bird_authors'),
    ]

    operations = [
        migrations.AddField(
            model_name='bird',
            name='authors',
            field=models.ManyToManyField(related_name='bird_authors', through='birds.AuthorBird', to=settings.AUTH_USER_MODEL),
        ),
    ]
# Generated by Django 3.1 on 2021-05-09 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0024_bird_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bird',
            name='created_at',
        ),
    ]

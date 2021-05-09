# Generated by Django 3.1 on 2021-05-09 14:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0023_auto_20210509_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='bird',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

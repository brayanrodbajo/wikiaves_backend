# Generated by Django 3.1 on 2021-07-16 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0060_auto_20210716_0627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bird',
            name='authors',
        ),
    ]

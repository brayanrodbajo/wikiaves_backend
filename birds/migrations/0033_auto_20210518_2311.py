# Generated by Django 3.1 on 2021-05-19 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0032_auto_20210518_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measure',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]

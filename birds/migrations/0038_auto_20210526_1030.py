# Generated by Django 3.1 on 2021-05-26 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0037_auto_20210526_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='description',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_description', to='birds.text'),
        ),
    ]

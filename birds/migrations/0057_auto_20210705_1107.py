# Generated by Django 3.1 on 2021-07-05 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0056_auto_20210630_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xenocanto',
            name='vocalization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='xenocantos', to='birds.vocalization'),
        ),
    ]
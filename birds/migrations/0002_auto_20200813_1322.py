# Generated by Django 3.0.5 on 2020-08-13 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bird',
            name='common_names',
            field=models.ManyToManyField(related_name='birds_cn', through='birds.CommonNameBird', to='birds.Text'),
        ),
        migrations.AlterField(
            model_name='family',
            name='common_names',
            field=models.ManyToManyField(through='birds.CommonNameFamily', to='birds.Text'),
        ),
        migrations.AlterField(
            model_name='order',
            name='common_names',
            field=models.ManyToManyField(through='birds.CommonNameOrder', to='birds.Text'),
        ),
    ]

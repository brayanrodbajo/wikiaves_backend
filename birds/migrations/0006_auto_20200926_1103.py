# Generated by Django 3.1 on 2020-09-26 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0005_auto_20200926_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bird',
            name='scientific_names',
        ),
        migrations.RemoveField(
            model_name='family',
            name='scientific_names',
        ),
        migrations.RemoveField(
            model_name='order',
            name='scientific_names',
        ),
        migrations.AlterField(
            model_name='scientificnamebird',
            name='bird',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scientific_names', to='birds.bird'),
        ),
        migrations.AlterField(
            model_name='scientificnamebird',
            name='name',
            field=models.CharField(default='name', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scientificnamefamily',
            name='family',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scientific_names', to='birds.family'),
        ),
        migrations.AlterField(
            model_name='scientificnamefamily',
            name='name',
            field=models.CharField(default='name', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scientificnameorder',
            name='name',
            field=models.CharField(default='name', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scientificnameorder',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scientific_names', to='birds.order'),
        ),
    ]
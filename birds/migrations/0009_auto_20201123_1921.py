# Generated by Django 3.1 on 2020-11-24 00:21

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0008_auto_20201005_1226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('unit', models.CharField(choices=[('cm', 'cm'), ('in', 'in'), ('gr', 'gr')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Subspecies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SubspeciesName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main', models.BooleanField(default=False)),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_name', to='birds.text')),
                ('subspecies', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='names', to='birds.subspecies')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inferior', models.FloatField(blank=True, null=True)),
                ('superior', models.FloatField(blank=True, null=True)),
                ('average', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='conservation',
            name='text',
        ),
        migrations.RemoveField(
            model_name='habitat',
            name='text',
        ),
        migrations.RemoveField(
            model_name='length',
            name='bird',
        ),
        migrations.RemoveField(
            model_name='sdfemale',
            name='image',
        ),
        migrations.RemoveField(
            model_name='sdfemale',
            name='text',
        ),
        migrations.RemoveField(
            model_name='sdmale',
            name='image',
        ),
        migrations.RemoveField(
            model_name='sdmale',
            name='text',
        ),
        migrations.RemoveField(
            model_name='sdsubadult',
            name='image',
        ),
        migrations.RemoveField(
            model_name='sdsubadult',
            name='text',
        ),
        migrations.RemoveField(
            model_name='sdyouth',
            name='image',
        ),
        migrations.RemoveField(
            model_name='sdyouth',
            name='text',
        ),
        migrations.RemoveField(
            model_name='sexualdifferentiation',
            name='female',
        ),
        migrations.RemoveField(
            model_name='sexualdifferentiation',
            name='male',
        ),
        migrations.RemoveField(
            model_name='sexualdifferentiation',
            name='subadult',
        ),
        migrations.RemoveField(
            model_name='sexualdifferentiation',
            name='youth',
        ),
        migrations.RemoveField(
            model_name='bird',
            name='behavior',
        ),
        migrations.RemoveField(
            model_name='bird',
            name='curiosities',
        ),
        migrations.RemoveField(
            model_name='bird',
            name='feeding',
        ),
        migrations.RemoveField(
            model_name='bird',
            name='sexual_differentiation',
        ),
        migrations.RemoveField(
            model_name='identification',
            name='regional_differences',
        ),
        migrations.RemoveField(
            model_name='identification',
            name='similar_species',
        ),
        migrations.RemoveField(
            model_name='identification',
            name='size_shape',
        ),
        migrations.RemoveField(
            model_name='image',
            name='author',
        ),
        migrations.RemoveField(
            model_name='image',
            name='bird',
        ),
        migrations.RemoveField(
            model_name='image',
            name='category',
        ),
        migrations.RemoveField(
            model_name='image',
            name='location',
        ),
        migrations.RemoveField(
            model_name='reproduction',
            name='type',
        ),
        migrations.AddField(
            model_name='bird',
            name='identification_similar',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='similar_species', to='birds.identification'),
        ),
        migrations.AddField(
            model_name='identification',
            name='description',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='identification_description', to='birds.text'),
        ),
        migrations.AlterField(
            model_name='author',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_image', to='birds.image'),
        ),
        migrations.AlterField(
            model_name='bird',
            name='habitat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bird', to='birds.text'),
        ),
        migrations.CreateModel(
            name='BirdImage',
            fields=[
                ('image_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='birds.image')),
                ('category', models.CharField(blank=True, choices=[('BIRD', 'BIRD'), ('FAMILY', 'FAMILY'), ('ORDER', 'ORDER')], max_length=6, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images_authored', to='birds.author')),
            ],
            bases=('birds.image',),
        ),
        migrations.DeleteModel(
            name='Feeding',
        ),
        migrations.DeleteModel(
            name='Habitat',
        ),
        migrations.DeleteModel(
            name='Length',
        ),
        migrations.DeleteModel(
            name='SDFemale',
        ),
        migrations.DeleteModel(
            name='SDMale',
        ),
        migrations.DeleteModel(
            name='SDSubadult',
        ),
        migrations.DeleteModel(
            name='SDYouth',
        ),
        migrations.DeleteModel(
            name='SexualDifferentiation',
        ),
        migrations.AddField(
            model_name='type',
            name='bird_behavior',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='behavior', to='birds.bird'),
        ),
        migrations.AddField(
            model_name='type',
            name='bird_feeding',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='feeding', to='birds.bird'),
        ),
        migrations.AddField(
            model_name='type',
            name='identification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plumage', to='birds.identification'),
        ),
        migrations.AddField(
            model_name='type',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type_image', to='birds.image'),
        ),
        migrations.AddField(
            model_name='type',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type_name', to='birds.text'),
        ),
        migrations.AddField(
            model_name='type',
            name='reproduction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='types', to='birds.reproduction'),
        ),
        migrations.AddField(
            model_name='type',
            name='text',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type_text', to='birds.text'),
        ),
        migrations.AddField(
            model_name='subspecies',
            name='bird',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subspecies_bird', to='birds.bird'),
        ),
        migrations.AddField(
            model_name='subspecies',
            name='distribution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subspecies_dist', to='birds.text'),
        ),
        migrations.AddField(
            model_name='measure',
            name='identification_lengths',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lengths', to='birds.identification'),
        ),
        migrations.AddField(
            model_name='measure',
            name='identification_weights',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weights', to='birds.identification'),
        ),
        migrations.AlterField(
            model_name='bird',
            name='conservation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bird', to='birds.type'),
        ),
        migrations.DeleteModel(
            name='Conservation',
        ),
        migrations.AddField(
            model_name='birdimage',
            name='bird',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='birds.bird'),
        ),
    ]

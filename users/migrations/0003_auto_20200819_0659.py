import os
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_auto_20200813_1708'),
    ]

    def generate_superuser(apps, schema_editor):
        from users.models import CustomUser

        DJANGO_SU_NAME = os.environ.get('DJANGO_SU_NAME')
        DJANGO_SU_EMAIL = os.environ.get('DJANGO_SU_EMAIL')
        DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SU_PASSWORD')

        superuser = CustomUser.objects.create_superuser(
            username=DJANGO_SU_NAME,
            email=DJANGO_SU_EMAIL,
            password=DJANGO_SU_PASSWORD)
        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser),
    ]

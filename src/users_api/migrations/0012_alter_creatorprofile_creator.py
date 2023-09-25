# Generated by Django 4.2.5 on 2023-09-24 23:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_api', '0011_alter_creatorprofile_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creatorprofile',
            name='creator',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='creator_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]

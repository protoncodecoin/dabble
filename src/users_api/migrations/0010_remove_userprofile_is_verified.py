# Generated by Django 4.2.5 on 2023-10-01 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_api', '0009_userprofile_is_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_verified',
        ),
    ]

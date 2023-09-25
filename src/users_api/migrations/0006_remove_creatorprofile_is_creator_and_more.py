# Generated by Django 4.2.5 on 2023-09-17 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_api', '0005_remove_userprofile_is_commonuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creatorprofile',
            name='is_creator',
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_creator',
            field=models.BooleanField(default=False),
        ),
    ]
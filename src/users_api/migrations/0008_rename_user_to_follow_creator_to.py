# Generated by Django 4.2.5 on 2023-10-01 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_api', '0007_remove_creatorprofile_creator_following_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='user_to',
            new_name='creator_to',
        ),
    ]

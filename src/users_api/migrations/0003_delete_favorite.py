# Generated by Django 4.2.5 on 2024-03-07 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_api', '0002_alter_creatorprofile_creator_logo_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]

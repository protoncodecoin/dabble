# Generated by Django 4.2.5 on 2024-03-05 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anime_api', '0009_anime_favorited_by_series_favorited_by_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='story',
            old_name='thumbnail',
            new_name='story_thumbnail',
        ),
    ]
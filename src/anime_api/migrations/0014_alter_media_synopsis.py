# Generated by Django 4.2.5 on 2024-03-07 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime_api', '0013_rename_story_thumbnail_story_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='synopsis',
            field=models.TextField(max_length=300),
        ),
    ]
# Generated by Django 4.2.5 on 2024-05-21 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_api', '0004_alter_creatorprofile_slug'),
        ('anime_api', '0007_alter_video_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='design',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_illustration', to='users_api.creatorprofile'),
        ),
        migrations.AlterField(
            model_name='text',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_text', to='users_api.creatorprofile'),
        ),
    ]

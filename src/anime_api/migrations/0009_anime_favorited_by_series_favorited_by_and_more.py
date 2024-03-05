# Generated by Django 4.2.5 on 2024-03-05 08:43

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('users_api', '0002_alter_creatorprofile_creator_logo_and_more'),
        ('anime_api', '0008_text_video_alter_anime_anime_thumbnail_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='favorited_by',
            field=models.ManyToManyField(blank=True, related_name='favorite_animes', to='users_api.userprofile'),
        ),
        migrations.AddField(
            model_name='series',
            name='favorited_by',
            field=models.ManyToManyField(blank=True, related_name='favorite_series', to='users_api.userprofile'),
        ),
        migrations.AddField(
            model_name='story',
            name='favorited_by',
            field=models.ManyToManyField(blank=True, related_name='favorite_stories', to='users_api.userprofile'),
        ),
        migrations.AlterField(
            model_name='anime',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='story',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]

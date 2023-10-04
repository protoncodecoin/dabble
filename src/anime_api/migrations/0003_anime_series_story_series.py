# Generated by Django 4.2.5 on 2023-10-04 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anime_api', '0002_remove_anime_series_remove_story_series'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='anime_api.series'),
        ),
        migrations.AddField(
            model_name='story',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='anime_api.series'),
        ),
    ]

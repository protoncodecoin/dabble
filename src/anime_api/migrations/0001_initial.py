# Generated by Django 4.2.5 on 2023-09-25 18:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series_name', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('series_poster', models.ImageField(upload_to='series/posters/%Y/%m/%d/')),
                ('synopsis', models.TextField(max_length=500)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='series_created', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
            ],
            options={
                'verbose_name_plural': 'Series',
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episode_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)])),
                ('episode_title', models.CharField(max_length=500)),
                ('description', models.TextField(blank=True, max_length=700)),
                ('episode_release_date', models.DateField(auto_now_add=True)),
                ('publish', models.BooleanField(default=True)),
                ('thumbnail', models.ImageField(blank=True, upload_to='stories/thumbnails/%Y/%m/%d/')),
                ('content', models.TextField()),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='anime_api.series')),
            ],
            options={
                'verbose_name': 'Story',
                'verbose_name_plural': 'Stories',
            },
        ),
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episode_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)])),
                ('episode_title', models.CharField(max_length=500)),
                ('description', models.TextField(blank=True, max_length=700)),
                ('episode_release_date', models.DateField(auto_now_add=True)),
                ('publish', models.BooleanField(default=True)),
                ('thumbnail', models.ImageField(blank=True, upload_to='animations/thumbnails/%Y/%m/%d')),
                ('file', models.FileField(upload_to='animations/video/%Y/%m/%d/', verbose_name='video file')),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='anime_api.series')),
            ],
            options={
                'verbose_name': 'Animation',
                'verbose_name_plural': 'Animations',
            },
        ),
    ]

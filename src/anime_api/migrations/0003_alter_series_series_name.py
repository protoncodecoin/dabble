# Generated by Django 4.2.5 on 2023-10-06 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime_api', '0002_alter_anime_file_alter_anime_thumbnail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='series_name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]

# Generated by Django 4.2.5 on 2024-05-21 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anime_api', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='series',
            name='slug',
        ),
    ]

# Generated by Django 4.2.5 on 2024-05-21 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_api', '0003_alter_creatorprofile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creatorprofile',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
    ]
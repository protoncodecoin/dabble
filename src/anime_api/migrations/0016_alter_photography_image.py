# Generated by Django 5.0.7 on 2024-07-29 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime_api', '0015_alter_photography_typeof'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photography',
            name='image',
            field=models.ImageField(upload_to='singles/photography/%Y/%m/'),
        ),
    ]

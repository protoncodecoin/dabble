# Generated by Django 4.2.5 on 2024-06-11 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_book_external_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
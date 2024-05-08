# Generated by Django 4.2.5 on 2024-05-05 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_api', '0001_initial'),
        ('library', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='favorited_by',
            field=models.ManyToManyField(related_name='favorited_books', to='users_api.creatorprofile'),
        ),
    ]
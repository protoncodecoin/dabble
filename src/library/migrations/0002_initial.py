# Generated by Django 4.2.5 on 2024-05-21 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('library', '0001_initial'),
        ('users_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users_api.creatorprofile'),
        ),
        migrations.AddField(
            model_name='book',
            name='favorited_by',
            field=models.ManyToManyField(blank=True, related_name='favorited_books', to='users_api.creatorprofile'),
        ),
    ]

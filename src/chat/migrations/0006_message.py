# Generated by Django 5.0.7 on 2024-08-01 22:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_rename_message_groupmessage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('has_been_seen', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_msg', to=settings.AUTH_USER_MODEL)),
                ('to_who', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_who', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
# Generated by Django 4.2.5 on 2023-10-01 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_api', '0006_remove_creatorprofile_followers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creatorprofile',
            name='creator_following',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='following_creators',
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_from', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_following', to='users_api.userprofile')),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_followers', to='users_api.creatorprofile')),
            ],
            options={
                'verbose_name_plural': 'Follow',
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='follows',
            field=models.ManyToManyField(blank=True, related_name='followers', through='users_api.Follow', to='users_api.creatorprofile'),
        ),
    ]

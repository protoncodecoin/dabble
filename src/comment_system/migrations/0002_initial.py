# Generated by Django 4.2.5 on 2024-04-29 02:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users_api', '0001_initial'),
        ('comment_system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='users_api.userprofile'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['-created'], name='comment_sys_created_894a0e_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['content_type', 'object_id'], name='comment_sys_content_b12262_idx'),
        ),
    ]
# Generated by Django 4.2.5 on 2024-05-21 14:32

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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='users_api.creatorprofile'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['-date_posted'], name='comment_sys_date_po_493377_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['content_type', 'object_id'], name='comment_sys_content_b12262_idx'),
        ),
    ]

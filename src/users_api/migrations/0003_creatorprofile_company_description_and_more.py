# Generated by Django 4.2.5 on 2023-09-15 15:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users_api', '0002_userprofile_creatorprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='creatorprofile',
            name='company_description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='creatorprofile',
            name='company_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='creatorprofile',
            name='company_website',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]

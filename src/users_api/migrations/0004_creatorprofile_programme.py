# Generated by Django 4.2.5 on 2024-05-21 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_api', '0003_creatorprofile_users_api_c_total_l_6e3496_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='creatorprofile',
            name='programme',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

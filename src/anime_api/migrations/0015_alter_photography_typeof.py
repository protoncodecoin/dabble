# Generated by Django 5.0.7 on 2024-07-29 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime_api', '0014_alter_photography_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photography',
            name='typeof',
            field=models.CharField(default='photography', max_length=15),
        ),
    ]

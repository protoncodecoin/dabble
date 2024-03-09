# Generated by Django 4.2.5 on 2024-03-09 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('anime_api', '0014_alter_media_synopsis'),
    ]

    operations = [
        migrations.CreateModel(
            name='Design',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('design', models.ImageField(upload_to='singles/designs/%Y/%m/')),
            ],
        ),
        migrations.AlterField(
            model_name='media',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'model__in': ('text', 'video', 'design')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='media',
            name='synopsis',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]

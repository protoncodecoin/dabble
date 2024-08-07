# Generated by Django 5.0.7 on 2024-07-29 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_alter_book_book_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_category',
            field=models.CharField(choices=[('other', 'Others'), ('history', 'History'), ('design-illustration', 'Design/Illustration'), ('animation', 'Animation'), ('videography', 'Videography'), ('photography', 'Photography'), ('typography', 'Typography'), ('advertising', 'Advertising'), ('research', 'Research')], default='other', max_length=100),
        ),
    ]

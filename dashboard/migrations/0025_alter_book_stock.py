# Generated by Django 4.1.7 on 2023-04-14 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0024_book_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='stock',
            field=models.IntegerField(),
        ),
    ]

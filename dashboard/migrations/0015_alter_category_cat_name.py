# Generated by Django 4.1.7 on 2023-03-31 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_alter_author_book_alter_category_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cat_name',
            field=models.CharField(choices=[('Fiction', 'fiction'), ('Novel', 'fovel'), (
                'Biography', 'fiography'), ('Story', 'ftory'), ('History', 'fistory')], max_length=100),
        ),
    ]

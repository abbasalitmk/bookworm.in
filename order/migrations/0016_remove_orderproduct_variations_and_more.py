# Generated by Django 4.1.7 on 2023-04-11 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_alter_variation_book'),
        ('order', '0015_remove_orderproduct_book_edition_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='variations',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variations',
            field=models.ManyToManyField(blank=True, to='dashboard.variation'),
        ),
    ]

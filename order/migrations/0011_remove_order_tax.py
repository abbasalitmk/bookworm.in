# Generated by Django 4.1.7 on 2023-04-11 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_rename_order_id_order_provider_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tax',
        ),
    ]

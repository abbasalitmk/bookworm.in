# Generated by Django 4.1.7 on 2023-04-11 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_alter_razorpay_payment_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_id',
            new_name='provider_order_id',
        ),
    ]

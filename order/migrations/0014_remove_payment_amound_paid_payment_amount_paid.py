# Generated by Django 4.1.7 on 2023-04-11 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_alter_payment_amound_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='amound_paid',
        ),
        migrations.AddField(
            model_name='payment',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]

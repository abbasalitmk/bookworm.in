# Generated by Django 4.1.7 on 2023-04-16 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0037_alter_coupon_coupon_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='coupon_text',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='discount_amount',
            field=models.IntegerField(),
        ),
    ]

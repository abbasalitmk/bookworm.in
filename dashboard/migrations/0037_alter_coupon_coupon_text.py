# Generated by Django 4.1.7 on 2023-04-16 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0036_alter_coupon_discount_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='coupon_text',
            field=models.CharField(blank=True, max_length=150, unique=True),
        ),
    ]

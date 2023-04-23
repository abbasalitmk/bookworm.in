# Generated by Django 4.1.7 on 2023-04-15 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0033_remove_bookvariation_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookvariation',
            name='book',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='variation', to='dashboard.book'),
        ),
        migrations.AlterField(
            model_name='bookvariation',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='bookvariation',
            name='variation_type',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

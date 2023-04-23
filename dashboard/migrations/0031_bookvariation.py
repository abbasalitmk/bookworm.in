# Generated by Django 4.1.7 on 2023-04-15 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0030_delete_bookvariation'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variation_type', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variation', to='dashboard.book')),
            ],
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-30 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_alter_image_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.book'),
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-30 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_rename_auther_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='language',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
    ]

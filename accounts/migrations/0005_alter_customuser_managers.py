# Generated by Django 4.1.7 on 2023-03-27 10:00

import accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_user_customuser'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', accounts.models.UserManager()),
            ],
        ),
    ]

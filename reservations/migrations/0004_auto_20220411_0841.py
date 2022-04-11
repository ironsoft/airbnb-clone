# Generated by Django 2.2.5 on 2022-04-10 23:41

import core.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_bookedday'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='bookedday',
            managers=[
                ('objects', core.managers.CustomUserManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='reservation',
            managers=[
                ('objects', core.managers.CustomUserManager()),
            ],
        ),
    ]
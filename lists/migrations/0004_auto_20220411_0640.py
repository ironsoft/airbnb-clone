# Generated by Django 2.2.5 on 2022-04-10 21:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_auto_20220410_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='list', to=settings.AUTH_USER_MODEL),
        ),
    ]

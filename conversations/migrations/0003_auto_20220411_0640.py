# Generated by Django 2.2.5 on 2022-04-10 21:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0002_auto_20220307_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='conversation', to=settings.AUTH_USER_MODEL),
        ),
    ]
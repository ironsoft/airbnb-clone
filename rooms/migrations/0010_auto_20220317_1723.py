# Generated by Django 2.2.5 on 2022-03-17 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0009_auto_20220307_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='room',
            name='guests',
            field=models.IntegerField(blank=True, help_text='How many people will be staying?', null=True),
        ),
    ]

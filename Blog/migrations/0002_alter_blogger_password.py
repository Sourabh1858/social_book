# Generated by Django 4.2.1 on 2023-05-18 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogger',
            name='password',
            field=models.IntegerField(max_length=8),
        ),
    ]

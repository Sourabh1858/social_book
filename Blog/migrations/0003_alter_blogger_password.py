# Generated by Django 4.2.1 on 2023-05-18 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_alter_blogger_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogger',
            name='password',
            field=models.CharField(max_length=8),
        ),
    ]

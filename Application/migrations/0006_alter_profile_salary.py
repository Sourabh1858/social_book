# Generated by Django 4.2.1 on 2023-05-18 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0005_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='salary',
            field=models.IntegerField(null=True),
        ),
    ]

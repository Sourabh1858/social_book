# Generated by Django 4.2.1 on 2023-05-20 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0005_uploadedblogs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedblogs',
            name='image',
            field=models.FileField(upload_to='testFiles/Blogs'),
        ),
        migrations.AlterField(
            model_name='uploadedblogs',
            name='title',
            field=models.CharField(max_length=500),
        ),
    ]

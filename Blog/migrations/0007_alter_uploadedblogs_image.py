# Generated by Django 4.2.1 on 2023-05-20 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0006_alter_uploadedblogs_image_alter_uploadedblogs_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedblogs',
            name='image',
            field=models.ImageField(upload_to='testFiles/Blogs'),
        ),
    ]

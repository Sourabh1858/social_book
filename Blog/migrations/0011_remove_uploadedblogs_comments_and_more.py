# Generated by Django 4.2.1 on 2023-05-22 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0010_alter_uploadedblogs_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedblogs',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='uploadedblogs',
            name='likes',
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Blog.blogger')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(blank=True, max_length=500)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Blog.blogger')),
            ],
        ),
    ]

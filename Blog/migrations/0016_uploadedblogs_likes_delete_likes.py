# Generated by Django 4.2.1 on 2023-05-24 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0015_rename_likes_likes_count_remove_comments_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedblogs',
            name='likes',
            field=models.ManyToManyField(related_name='post_likes', to='Blog.blogger'),
        ),
        migrations.DeleteModel(
            name='Likes',
        ),
    ]

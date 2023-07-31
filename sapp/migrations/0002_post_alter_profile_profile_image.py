# Generated by Django 4.2.3 on 2023-07-16 08:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('post_image', models.ImageField(upload_to='post_images')),
                ('caption', models.TextField()),
                ('no_of_likes', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='default/blank-profile-picture.png', upload_to='profile_images'),
        ),
    ]
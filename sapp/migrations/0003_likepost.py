# Generated by Django 4.2.3 on 2023-07-16 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sapp', '0002_post_alter_profile_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=500)),
                ('username', models.CharField(max_length=100)),
            ],
        ),
    ]

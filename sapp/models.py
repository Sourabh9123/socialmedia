from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime

# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Profile_uuid = models.UUIDField(primary_key=True ,default=uuid.uuid4, editable=False,)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images', default="default/blank-profile-picture.png")
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.user.username
    


class Post(models.Model):
    post_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.CharField(max_length=100)
    post_image = models.ImageField(upload_to="post_images")
    caption = models.TextField()
    no_of_likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user
    


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)


    def __str__(self):
        return self.username
    



class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)



    def __str__(self):
        return self.user
    
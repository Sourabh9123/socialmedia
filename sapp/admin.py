from django.contrib import admin
from sapp.models  import Profile, Post, LikePost, FollowersCount


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','Profile_uuid', 'bio','profile_image', 'location','created_at','updated_at']
    list_display_links = ['user','location','profile_image','Profile_uuid']
    search_fields = ['location', 'Profile_uuid','user']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user','post_image','caption','no_of_likes','post_uuid', 'created_at','updated_at']
    list_display_links = ['user','post_image','post_uuid']
    search_fields = ['post_uuid','user']


@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'username']
    list_display_links = ['post_id', 'username']
    search_fields = ['post_id', 'username']


@admin.register(FollowersCount)
class FollowersCountAdmin(admin.ModelAdmin):
    list_display = ['follower', 'user']
    list_display_links = ['follower', 'user']
    search_fields =  ['follower', 'user']
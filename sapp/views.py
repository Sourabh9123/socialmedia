from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from sapp.models import Profile, Post, LikePost, FollowersCount
from django.contrib.auth.decorators import login_required 

from itertools import chain
import random

from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect





#made by me logout required
##############################

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def logout_required(view_func):
    """
    Decorator for views that can only be accessed by anonymous users (not logged in).
    If a logged-in user tries to access a view with this decorator, they will be redirected to a specified URL.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            # If the user is logged in, redirect them to a specific URL.
            return redirect('home')  # Replace 'some_redirect_url' with the URL you want to redirect to.

        # If the user is not logged in, call the original view.
        return view_func(request, *args, **kwargs)

    return _wrapped_view
##############################









@login_required(login_url='login')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')


    post = Post.objects.get(post_uuid=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        return redirect('home')
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect('home')
    return render (request, 'home.html')





def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_posts_length = len(user_posts)

    follower = request.user.username
    user = pk
    if FollowersCount.objects.filter(user=user, follower=follower).first():
        button_text = 'Unfollow'
    else:
        button_text = 'follow' 

    user_folowers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))
    context = {
        'user_posts_length':user_posts_length,
        'user_posts':user_posts,
        'user_object': user_object,
        'user_profile' : user_profile, 
        'button_text' : button_text,
        'user_folowers':user_folowers,
        'user_following':user_following,
    } 
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def follow(request):
    if request.method == "POST":
        follower = request.POST['follower']
        user = request.POST['user']
        
        print(request.user.username)
        

        
        if FollowersCount.objects.filter(user=user, follower=follower).first():
                delete_follower = FollowersCount.objects.get(follower=follower, user=user)
                delete_follower.delete()
                return redirect(f'/profile/{user}')
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect(f'/profile/{user}')

    else:
        return redirect('home')




@login_required(login_url='login')
def home(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    posts = Post.objects.all()
    user_following_list = []
    feed = []
    user_following = FollowersCount.objects.filter(follower=request.user.username)
    
    for users in user_following:
        user_following_list.append(users.user)
       
    for username in user_following_list:
       
        feed_lists = Post.objects.filter(user=username)
       
        feed.append(feed_lists)
    
   
    feed_list = list(chain(*feed))

    # user suggestions 
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [ x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(user_id=ids)
        username_profile_list.append(profile_lists)


    sugeestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'home.html', {'user_profile':user_profile, "posts":feed_list,'sugeestions_username_profile_list':sugeestions_username_profile_list[:5]})

@logout_required
@transaction.atomic()
def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        print(username,  email,  password , confirm_password)
        if password == confirm_password :
            if User.objects.filter(Q(email=email) | Q(username= username)).exists():
                messages.info(request, "Email or Username Already exists")
                return redirect('signup')
            # elif User.objects.filter(username=username).exists():
            #     messages.info(request, "Username is taken ")
            #     return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                #loin user and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request , user_login)
 

                # creating profile objects for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('settings')
                
            pass
        else:
            messages.info(request, "password and confirm password doesn't match")
            return redirect('signup')
            

    
    # else:
    #     return render(request, 'signup')
    


    return render(request, 'signup.html')



def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return  redirect('home')
        else:
            messages.info(request, "Invalid Credentials")
            return redirect('login')

        print(password, username)

    return render(request, 'login.html')




@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')



@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        if request.FILES.get('image') == None:
            image = user_profile.profile_image
            bio = request.POST['bio']
            location = request.POST['location']
            user_profile.profile_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        elif request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            user_profile.profile_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            return redirect('settings')
        


    return render(request,  'settings.html', {"user_profile":user_profile,
                                              
                                              })


def upload(request):

    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image')
        captions = request.POST['captions']
        new_post = Post.objects.create(user=user, caption=captions, post_image=image)
        new_post.save()
        return redirect('home')
    # else:
    #     return redirect('home')

    return render(request, 'uploadpost.html')



@login_required(login_url='login')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":
        username = request.POST.get('username')
        # username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = Profile.objects.filter(
            user__username__icontains=username
        ).only("user", "location", "bio", "profile_image")

        # for users in username_object:
        #     username_profile.append(users.id)

        # for ids in username_profile:
        #     profile_lists = Profile.objects.filter(user_id=ids)
        #     username_profile_list.append(profile_lists)


        # username_profile_list = list(chain(*username_profile_list))
        print(username_profile_list)



    return  render(request, 'search.html', {'username_profile_list':username_profile_list})






def delete_post(request, post_uuid):
    user = request.user
    
    try:
        post = Post.objects.get(pk=post_uuid)
        post_owner = post.user
        
        
        # Check if the user is the owner of the post
        if str(user) == post_owner:
            # User is the owner, allow deletion
            post.delete()
            print('Post deleted successfully.________________________________')

            return redirect(f"/profile/{user.username}")
        

        else:
            # User is not the owner, handle unauthorized deletion attempt
            print('Unauthorized deletion attempt. You are not the owner of this post.')
            # Optionally, you can raise a PermissionDenied exception here if you want to handle it in the template.
            # from django.core.exceptions import PermissionDenied
            # raise PermissionDenied("You are not authorized to delete this post.")

    except Post.DoesNotExist:
        # Post with the provided post_uuid does not exist, handle as needed
        print('The post does not exist.')
        return redirect('home')
    
    return redirect('f"/profile/{user.username}"')
    

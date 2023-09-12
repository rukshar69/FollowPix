from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount, Notification
from itertools import chain
import random
from django.http import JsonResponse
# Create your views here.

@login_required(login_url='signin')
def index(request):
    # Retrieve the currently logged in user object
    user_object = User.objects.get(username=request.user.username)
    
    # Retrieve the profile of the currently logged in user
    user_profile = Profile.objects.get(user=user_object)

    # Initialize empty lists
    user_following_list = []
    feed = []

    # Retrieve the users that the current user is following
    user_following = FollowersCount.objects.filter(follower=request.user.username)

    # Add usernames of the users that the current user is following to a list
    for users in user_following:
        user_following_list.append(users.user)

    # Retrieve posts of each user that the current user is following and add them to the feed list
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    # Flatten the nested feed list into a single-level list
    feed_list = list(chain(*feed))

    # Retrieve all user objects
    all_users = User.objects.all()
    
    # Initialize an empty list for all users that the current user is following
    user_following_all = []

    # Retrieve user objects for each user that the current user is following
    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    # Generate a list of new user suggestions that the current user is not following
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    
    # Retrieve the current user object
    current_user = User.objects.filter(username=request.user.username)
    
    # Filter out the current user from the new suggestions list
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    
    # Shuffle the list of final suggestions
    random.shuffle(final_suggestions_list)

    # Initialize empty lists
    username_profile = []
    username_profile_list = []

    # Retrieve the ids of user profiles in the final suggestions list
    for users in final_suggestions_list:
        username_profile.append(users.id)

    # Retrieve profile objects for each id in the username_profile list and add them to the username_profile_list
    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    # Flatten the nested username_profile_list into a single-level list
    suggestions_username_profile_list = list(chain(*username_profile_list))

    user_profile = get_object_or_404(Profile, user__username=request.user.username)
    # Retrieve the 5 most recent notifications for the logged-in user
    notifications = Notification.objects.filter(recipient=user_profile).order_by('-timestamp')[:5]


    # Render the 'index.html' template with the user profile, feed list, and list of suggested user profiles
    return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4], 'notifications': notifications})

@login_required(login_url='signin')
def follower_list(request):
    profile_username = request.GET.get('profile_username')
    # Retrieve the currently logged in user object
    user_object = User.objects.get(username=profile_username)

    # Retrieve the profile of the currently logged in user
    user_profile = Profile.objects.get(user=user_object)

    # Retrieve all users that are followers of the current user
    user_followers = FollowersCount.objects.filter(user=profile_username)
    user_followers_profile_list = []
    for follower in user_followers:
        #user_followers_id_list.append(follower.follower)
        follower_user = User.objects.get(username=follower.follower)
        follower_profile = Profile.objects.get(user=follower_user)
        user_followers_profile_list.append(follower_profile)
    
    
    print(user_followers_profile_list)
    context = {
        'user_followers': user_followers_profile_list,
        'user_profile': user_profile,
    }
    return render(request, 'search_follower.html', context)

@login_required(login_url='signin')
def following_list(request):
    # Retrieve the currently logged in user object
    profile_username = request.GET.get('profile_username')
    user_object = User.objects.get(username=profile_username)

    # Retrieve the profile of the currently logged in user
    user_profile = Profile.objects.get(user=user_object)

    # Retrieve all users that are followers of the current user
    user_following = FollowersCount.objects.filter(follower=profile_username)
    user_following_profile_list = []
    for user in user_following:
        #user_followers_id_list.append(follower.follower)
        following_user = User.objects.get(username=user.user)
        following_profile = Profile.objects.get(user=following_user)
        user_following_profile_list.append(following_profile)
    
    
    print(user_following_profile_list)
    context = {
        'user_following': user_following_profile_list,
        'user_profile': user_profile,
    }
    return render(request, 'search_following.html', context)



# Define a view function called 'search' that requires user authentication.
# If the user is not logged in, they will be redirected to the 'signin' URL.
@login_required(login_url='signin')
def search(request):
    # Get the User object associated with the currently logged-in user.
    user_object = User.objects.get(username=request.user.username)

    # Get the Profile object associated with the currently logged-in user.
    user_profile = Profile.objects.get(user=user_object)

    # Check if the HTTP request method is POST (typically when a form is submitted).
    if request.method == 'POST':
        # Get the 'username' value from the submitted form data.
        username = request.POST['username']

        # Use a case-insensitive filter to retrieve User objects whose usernames contain the provided value.
        username_object = User.objects.filter(username__icontains=username)

        # Initialize two empty lists to store user profiles and user IDs.
        username_profile = []
        username_profile_list = []

        # Iterate through the filtered User objects.
        for users in username_object:
            # Append the user IDs to the 'username_profile' list.
            username_profile.append(users.id)

        # Iterate through the user IDs obtained above.
        for ids in username_profile:
            # Use a filter to retrieve Profile objects based on user IDs and append them to the 'username_profile_list'.
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        # Flatten the nested list of Profile objects into a single list.
        username_profile_list = list(chain(*username_profile_list))

    # Render the 'search.html' template and provide the 'user_profile' and 'username_profile_list' as context data.
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower_username = request.POST['follower']
        user_username = request.POST['user']

        # Get the Profile objects for follower and user
        follower_profile = get_object_or_404(Profile, user__username=follower_username)
        user_profile = get_object_or_404(Profile, user__username=user_username)

        if FollowersCount.objects.filter(follower=follower_username, user=user_username).first():
            delete_follower = FollowersCount.objects.get(follower=follower_username, user=user_username)
            delete_follower.delete()

            

            return redirect('/profile/' + user_username)
        else:
            new_follower = FollowersCount.objects.create(follower=follower_username, user=user_username)
            new_follower.save()

            # Create a notification instance for the follow action
            notification_type = 'follow'

            notification = Notification.objects.create(
                recipient=user_profile,
                sender=follower_profile,
                notification_type=notification_type,
            )
            notification.save()

            return redirect('/profile/' + user_username)
    else:
        return redirect('/')


@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    user_profile = Profile.objects.get(user=request.user)

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        
        is_liked = True

        # Get the User object associated with the post's owner
        post_owner_user = User.objects.get(username=post.user)
        # Get the Profile associated with the User object
        recipient_profile = Profile.objects.get(user=post_owner_user)
        post = Post.objects.get(id=post_id) #get the post object to be saved in notification

        # Create a notification for the post owner
        notification = Notification.objects.create(
            sender=user_profile,
            recipient=recipient_profile,
            notification_type='like',
            post = post,
        )
        notification.save()
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        is_liked = False

        # Get the User object associated with the post's owner
        post_owner_user = User.objects.get(username=post.user)
        # Get the Profile associated with the User object
        recipient_profile = Profile.objects.get(user=post_owner_user)

        

    data = {
        'liked': is_liked,
        'like_count': post.no_of_likes,
    }

    return JsonResponse(data)
    

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def settings(request):
    # Retrieve the user's profile object
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        # Update the profile information if a POST request is received
        
        # Check if an image file is provided in the request
        if request.FILES.get('image') == None:
            # If no image is provided, retain the existing profile image
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            # Update the profile information
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            # If an image is provided, update the profile image with the new image
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            # Update the profile information
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        # Redirect the user to the settings page
        return redirect('settings')

    # Render the settings page with the user's profile information
    return render(request, 'setting.html', {'user_profile': user_profile})
def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
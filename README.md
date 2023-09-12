# FollowPix
A Django app where users share photos and reactions. Here, users upload photos for their followers to view and like. They can also search for other users, view their profiles, photos, and follow them.

## Sample Deployment
Deployed to PythonAnywhere: [ruksharahmed7.pythonanywhere.com](http://ruksharahmed7.pythonanywhere.com/)

## Features
- Basic authentication using Django's default user model
- [Homepage](http://ruksharahmed7.pythonanywhere.com/)(requires login) lists latest posts from the users followed by the logged in user. Each post displays the photo, a caption, and the number of likes. The user can like/unlike the post.
    - On the right, there is a list of suggested users to follow. 
    - In the header, there is a search bar to search for users by username. The search results are a list of users.
    - On the top right, there is a user photo thumbnail. Clicking on it shows 3 options:
        - Profile page
        - Account Settings
        - Logout
    - On the right, there is a button to upload a photo along with its caption.
    - There is a notification button as well which lets you view the 5 most recent notifications. There are 2 types of notifications:
        - If someone is following you
        - If someone has liked the logged in user's photo

![Profile thumbnail header options](https://github.com/rukshar69/FollowPix/blob/main/images_readme/notifications_d.png)

![Profile thumbnail header options](https://github.com/rukshar69/FollowPix/blob/main/images_readme/1.png)
    
    

![Profile thumbnail header options](https://github.com/rukshar69/FollowPix/blob/main/images_readme/2.png)
- Profile page shows user details, follower and following count, and a list of photos, along with its caption and like count, uploaded by the user. Clicking on a photo opens it in a lightbox. Clicking on the follower and following count will show the list of followers and following users.
- Account settings allows the user to add profile photo, location, and bio.
- Some example usernames and passwords are provided in [users.txt](https://github.com/rukshar69/FollowPix/blob/main/social_book/users.txt)
- In order to prevent page-reload after liking a post, **jQuery/Ajax** is used in [index.html](http://ruksharahmed7.pythonanywhere.com/), the page for post-feed. Now, only the like-count will change and the rest will remain as it is.

## Reference
- [django-social-media-website](https://github.com/tomitokko/django-social-media-website)
- [django-social-media-template ](https://github.com/tomitokko/django-social-media-template)
- [Deploy a Django web app to Python Anywhere](https://www.youtube.com/watch?v=xtnUwvjOThg)
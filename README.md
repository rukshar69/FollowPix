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

![Profile thumbnail header options](https://github.com/rukshar69/FollowPix/blob/main/images_readme/1.png)
    
    

![Profile thumbnail header options](https://github.com/rukshar69/FollowPix/blob/main/images_readme/2.png)
- Profile page shows user details, follower and following count, and a list of photos uploaded by the user.
- Account settings allows the user to add profile photo, location, and bio.
- Some example usernames and passwords are provided in [users.txt](https://github.com/rukshar69/FollowPix/blob/main/social_book/users.txt)

## Reference
- [django-social-media-website](https://github.com/tomitokko/django-social-media-website)
- [django-social-media-template ](https://github.com/tomitokko/django-social-media-template)
- [Deploy a Django web app to Python Anywhere](https://www.youtube.com/watch?v=xtnUwvjOThg)
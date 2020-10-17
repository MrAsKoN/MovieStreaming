# MovieStreaming

A responsive web application for movie streaming where users can watch any movies, comments their opinions about the movies and admins can add movies, modify movie content etc. The application is built using Django, Pyrebase and firebase-admin SDK.
Pyrebase was used for accessing firebase storage and authentication. firebase-admin SDK was used for accessing Cloud Firestore.


### Responsive Web Page
![register](/images/responsive.JPG)


## Functionality

Users can register in the application.
![register](/images/register.JPG)


Further, users and admin can log in. Firebase Authentication was used to authenticate users and admin.
![register](/images/login.JPG)


Both admin and users can watch select from any of the available movies.
![register](/images/user_home.JPG)


Also, they can comment their opinions for every movie. These comments are public and are visible to every other authenticated user and the admin.
![register](/images/comment.JPG)


Admin can add new movies, update existing movie details and even delete the movies.
![register](/images/admin_home.JPG)


Admin can add a new movie by specifying the each and every detail about the movie including the embedded contentURL.
![register](/images/addmovies.JPG)


Similarly, admin can update details of any movie by modifying the 'Update Movies' form.
![register](/images/updateform.JPG)


Lastly, admin can also delete movies.
![register](/images/deletemovie.JPG)


## Database Structure

### Users Schema
![register](/images/users-schema.JPG)


### Movies Schema
![register](/images/movie-schema.JPG)


### Comments Schema
![register](/images/comments-schema.JPG)


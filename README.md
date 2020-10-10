# MovieStreaming

A responsive web application for movie streaming where users can watch any movies, comments their opinions about the movies and admins can add movies, modify movie content etc. The application is built using Django, Pyrebase and firebase-admin SDK.
Pyrebase was used for accessing firebase storage and authentication. firebase-admin SDK was used for accessing Cloud Firestore.

#Functionality

Users can register in the application.

Further, users and admin can log in. Firebase Authentication was used to authenticate users and admin.

Both admin and users can watch select from any of the available movies.

Also, they can comment their opinions for every movie. These comments are public and are visible to every other authenticated user and the admin.

Admin can add new movies, update existing movie details and even delete the movies.

Admin can add a new movie by specifying the each and every detail about the movie including the embedded contentURL.

Similarly, admin can update details of any movie by modifying the 'Update Movies' form.

Lastly, admin can also delete movies.


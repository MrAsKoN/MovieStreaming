from django.shortcuts import render, redirect
from config import db


def home(request):
    if 'uid' in request.session:  # if user is authenticated
        user = db.collection('users').document(request.session['uid']).get().to_dict()  # retreive current user details
        if user['isAdmin']:  # check if user is Admin
            return redirect('adminhome') #redirect him/her to adminhome
        movies = db.collection('movies').get() #retreive movies from cloud firestore

        moviesdata = []
        for movie in movies:
            moviesdata.append(movie.to_dict()) #convert document references to dictionary

        return render(request, 'users/home.html', context={"moviesdata": moviesdata}) #render home template with movies data in context
    return redirect('login') #if user isnt authenticated redirect him/her to login page


def movie(request, id):
    if 'uid' in request.session: #if user is authenticated let him/her in
        movie = db.collection('movies').document(id).get() #retreive the particular movie details on which the user clicked from cloud firestore
        comments = db.collection('movies').document(id).collection('comments').get() #retreive comments of the particular movie on which the user clicked from cloud firestore
        commentsdata = []
        for comment in comments:
            commentsdata.append(comment.to_dict()) #convert comments data from document references to dictionary
        print(commentsdata)
        return render(request, 'users/movie.html',context={"movie": movie.to_dict(), "comments": commentsdata})  #render movie template with movie details and comments data in context
    return redirect('login')  #if user isnt authenticated redirect him/her to login page


def comment(request, id):
    if 'uid' in request.session: #if user is authenticated let him/her in
        if request.method == 'POST': #if POST request
            comment = request.POST.get('comment') #retreive comment in textarea
            if comment: #if comment is not empty
                curruser = db.collection('users').document(request.session['uid']).get() #retrieve current user details

                db.collection('movies').document(id).collection('comments').add(  #add the comment to comments part of that particular movie
                    {"uid": request.session['uid'], "comment": comment, "username": curruser.to_dict()['username']})
        return redirect('movie',id=id) #if no POST request then redirect to the same page
    return redirect('login') #if user isnt authenticated redirect him/her to login page

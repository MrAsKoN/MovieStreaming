from django.shortcuts import render, redirect
from config import db


def home(request):
    if 'uid' in request.session:
        movies = db.collection('movies').get()

        moviesdata = []
        for movie in movies:
            moviesdata.append(movie.to_dict())

        return render(request, 'users/home.html', context={"moviesdata": moviesdata, 'uid': request.session['uid']})
    return redirect('login')


def movie(request, id):
    if 'uid' in request.session:
        movie = db.collection('movies').document(id).get()
        comments = db.collection('movies').document(id).collection('comments').get()
        commentsdata = []
        for comment in comments:
            commentsdata.append(comment.to_dict())
        print(commentsdata)
        return render(request, 'users/movie.html',
                      context={"movie": movie.to_dict(), "comments": commentsdata})
    return redirect('login')


def comment(request, id):
    if 'uid' in request.session:
        if request.method == 'POST':
            comment = request.POST.get('comment')
            if comment:
                curruser = db.collection('users').document(request.session['uid']).get()

                db.collection('movies').document(id).collection('comments').add(
                    {"uid": request.session['uid'], "comment": comment, "username": curruser.to_dict()['username']})
        return redirect('movie', id=id)
    return redirect('login')

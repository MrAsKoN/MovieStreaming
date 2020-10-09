from django.shortcuts import render, redirect
from config import db, storage

def adminhome(request):
    if 'uid' in request.session:
        user = db.collection('users').document(request.session['uid']).get().to_dict()
        print(user)
        if user['isAdmin']:
            movies = db.collection('movies').get()
            moviesdata = []
            for movie in movies:
                moviesdata.append(movie.to_dict())
            return render(request,'admin/home.html',context={"moviesdata": moviesdata, 'uid':request.session['uid']})
        return redirect('home')
    return redirect('login')
def addmovies(request):
    if 'uid' in request.session:
        user = db.collection('users').document(request.session['uid']).get().to_dict()
        print(user)
        if user['isAdmin']:
            if request.method == 'POST':
                name = request.POST.get('name')
                genre = request.POST.get('genre')
                contentrating = request.POST.get('contentrating')
                contentURL = request.POST.get('contentURL')
                poster = request.FILES['poster']
                releasedate = request.POST.get('releasedate')

                if (name and genre and contentrating and contentURL and releasedate):
                    if 'poster' in request.FILES:
                        storage.child('movies/posters/' + name).put(poster)
                        posterURL = storage.child("movies/posters/" + name).get_url(None)

                        movie = {'name': name, 'genre': genre, 'contentrating': contentrating,
                                 'contentURL': contentURL,
                                 'poster': posterURL, 'releasedate': releasedate}
                        print(movie)
                        doc = db.collection('movies').document()
                        doc_id = doc.id
                        movie['id'] = doc_id
                        doc.set(movie)
                        return redirect('home')
            return render(request, 'admin/addmovies.html')
        return redirect('home')
    return render(request, 'authentication/login.html')


def modifymovies(request):
    if 'uid' in request.session:
        user = db.collection('users').document(request.session['uid']).get().to_dict()
        print(user)
        if user['isAdmin']:
            movies = db.collection('movies').get()
            moviesdata = []
            for movie in movies:
                moviesdata.append(movie.to_dict())
            return render(request, 'admin/modifymovies.html', context={"movies": moviesdata})
        return redirect('home')
    return redirect('login')


def updatemovie(request, id):
    if 'uid' in request.session:
        user = db.collection('users').document(request.session['uid']).get().to_dict()
        print(user)
        if user['isAdmin']:
            movie = db.collection('movies').document(id).get().to_dict()
            return render(request, 'admin/updatemovie.html', context={"movie": movie})
        return redirect('home')
    return redirect('login')


def updatedone(request, id):
    if 'uid' in request.session:
        user = db.collection('users').document(request.session['uid']).get().to_dict()

        if user['isAdmin']:

            if request.method == 'POST':
                print("inside")
                name = request.POST.get('name')
                genre = request.POST.get('genre')
                contentrating = request.POST.get('contentrating')
                contentURL = request.POST.get('contentURL')
                releasedate = request.POST.get('releasedate')

                if name and genre and contentrating and contentURL and releasedate:
                    if 'poster' in request.FILES:
                        poster = request.FILES['poster']
                        storage.child('images/posters/' + name).put(poster)
                        posterURL = storage.child('images/posters/' + name).get_url(None)
                        movie = {'name': name, 'genre': genre, 'contentrating': contentrating,
                                 'contentURL': contentURL,
                                 'poster': posterURL, 'releasedate': releasedate}
                        db.collection('movies').document(id).update(movie)
                    else:
                        print("no poster")
                        movie = {'name': name, 'genre': genre, 'contentrating': contentrating,
                                 'contentURL': contentURL, 'releasedate': releasedate}
                        db.collection('movies').document(id).update(movie)
                    return redirect('modifymovies')
            return redirect('updatemovie')
        return redirect('home')
    return render(request, 'authentication/login.html')


def deletemovies(request, id):
    if 'uid' in request.session:
        user = db.collection('users').document(request.session['uid']).get().to_dict()
        if user['isAdmin']:
            movie = db.collection('movies').document(id).delete()
            return redirect('modifymovies')
        return redirect('home')
    return redirect('login')


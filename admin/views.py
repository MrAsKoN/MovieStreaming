from django.shortcuts import render, redirect
from config import db, storage


def adminhome(request):
    if 'uid' in request.session:  # if user is authenticated
        user = db.collection('users').document(request.session['uid']).get().to_dict()  # retreive current user details
        if user['isAdmin']:  # check if user is Admin
            movies = db.collection('movies').get()  # retreive movie details

            moviesdata = []
            for movie in movies:
                moviesdata.append(movie.to_dict())  # convert document references to dictionary

            return render(request, 'admin/home.html',
                          context={"moviesdata": moviesdata, 'uid': request.session['uid']})  # render admin's home page
        return render(request,'users/home.html',context={'uid':request.session['uid']})  # if user is not an admin then redirect him/her to user home page
    return redirect('login')  # if user isnt authenticated redirect him/her to login page


def addmovies(request):
    if 'uid' in request.session:  # if user is authenticated
        user = db.collection('users').document(request.session['uid']).get().to_dict()  # retreive current user details
        if user['isAdmin']:  # check if user is Admin
            if request.method == 'POST':  # if POST request
                name = request.POST.get('name')
                genre = request.POST.get('genre')
                contentrating = request.POST.get('contentrating')  # retreive details from input fields
                contentURL = request.POST.get('contentURL')
                poster = request.FILES['poster']
                releasedate = request.POST.get('releasedate')
                description = request.POST.get('description')
                if (name and genre and contentrating and contentURL and releasedate and description):  # if all fields are non empty
                    if 'poster' in request.FILES:  # if poster(image) exists

                        storage.child('movies/posters/' + name).put(poster)  # add image to firebase storage
                        posterURL = storage.child("movies/posters/" + name).get_url(None)  # generate url for that image

                        movie = {'name': name, 'genre': genre, 'contentrating': contentrating,
                                 'contentURL': contentURL,
                                 'poster': posterURL, 'releasedate': releasedate, 'description': description}

                        doc = db.collection('movies').document()  # create a document
                        doc_id = doc.id  # generate unique id
                        movie['id'] = doc_id
                        doc.set(movie)  # add all details to firebase
                        return redirect('adminhome')  # redirect to admin home
            return render(request, 'admin/addmovies.html')  # if no POST request, then redirect to same page
        return redirect('home')  # if user is not admin, redirect to user's home page
    return redirect('login')  # if user is not authenticated, then redirect to login page


def updatemovie(request, id):
    if 'uid' in request.session:  # if user is authenticated
        user = db.collection('users').document(request.session['uid']).get().to_dict()  # retreive current user details

        if user['isAdmin']:  # check if user is Admin
            movie = db.collection('movies').document(id).get().to_dict()  # retreive that particular movie with given id
            return render(request, 'admin/updatemovie.html',context={"movie": movie})  # pass movie details for further updating movie details
        return redirect('home')  # if user is not admin, redirect to user's home page
    return redirect('login')  # if user is not authenticated, then redirect to login page


def updatedone(request, id):
    if 'uid' in request.session:  # if user is authenticated
        user = db.collection('users').document(request.session['uid']).get().to_dict()  # retreive current user details

        if user['isAdmin']:  # check if user is Admin

            if request.method == 'POST':  # if POST request
                name = request.POST.get('name')
                genre = request.POST.get('genre')
                contentrating = request.POST.get('contentrating')  # retreive updated movie details from input fields
                contentURL = request.POST.get('contentURL')
                releasedate = request.POST.get('releasedate')

                if name and genre and contentrating and contentURL and releasedate:  # if all fields are non empty

                    if 'poster' in request.FILES:  # if new poster image exits
                        poster = request.FILES['poster']
                        storage.child('images/posters/' + name).put(poster)  # store the new image in firebase storage
                        posterURL = storage.child('images/posters/' + name).get_url(
                            None)  # retreive new url for new image

                        movie = {'name': name, 'genre': genre, 'contentrating': contentrating,
                                 'contentURL': contentURL,
                                 'poster': posterURL, 'releasedate': releasedate}
                    else:
                        movie = {'name': name, 'genre': genre, 'contentrating': contentrating,
                                 # if no new poster exists
                                 'contentURL': contentURL, 'releasedate': releasedate}
                    db.collection('movies').document(id).update(movie)  # update details in the database
                    return redirect('adminhome')  # After successfully updating movie details return
            return redirect('updatemovie',id=id)
        return redirect('home')
    return render(request, 'authentication/login.html')


def deletemovies(request, id):
    if 'uid' in request.session:  # if user is authenticated
        user = db.collection('users').document(request.session['uid']).get().to_dict()  # retreive current user details

        if user['isAdmin']:  # check if user is Admin
            movie = db.collection('movies').document(
                id).delete()  # retreive movie document for particular id and delete it from database
            return redirect('adminhome')  # redirect to admin home page
        return redirect('home')  # if user is not admin then return to user's home page
    return redirect('login')  # if user is not authenticated then redirect to home page

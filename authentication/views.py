from django.contrib import messages
from django.shortcuts import render, redirect
from config import pyfirebase, db, auth


def register(request):
    if request.method == 'POST': #if POST request
        username = request.POST.get('username')
        email = request.POST.get('email')   #collect data from respective input fields
        password = request.POST.get('password')
        user = None
        if not (username and email and password): #if any field is empty redirect to register page again
            return render(request, 'authentication/register.html')
        try:
            user = auth.create_user(email=email, password=password) #create user using firebase-admin.auth()
        except:
            messages.error(request, "User Already exists!") # If user exists then, error is thrown.
            return render(request, 'authentication/register.html') #redirect to register page again

        data = {"username": username, "email": email, 'isAdmin': False}
        db.collection('users').document(user.uid).set(data) #add user data to cloud firestore database
        return redirect('home') #After successfully creating user and adding user's credentials to the database redirect to home page
    return render(request, 'authentication/register.html') #If no POST request, then redirect to register page again


def login(request):
    if request.method == 'POST': #if POST request
        email = request.POST.get('email')
        password = request.POST.get('password') #retreive details from input fields
        user = None

        if (email and password): #if details retreived are non-empty
            try:
                user = pyfirebase.auth().sign_in_with_email_and_password(email, password) #using firebase authentication to authenticate user via pyrebase
            except:
                messages.error(request,"Invalid Credentials") #error is occured if details are invalid
                return render(request, 'authentication/login.html') # in that case redirect to login page again

            session_id = user['localId']
            request.session['uid'] = session_id #store uid in session variable for future authentication
            user = db.collection('users').document(request.session['uid']).get().to_dict()  # retreive current user details

            if user['isAdmin']:  # check if user is Admin

                return redirect('adminhome') #if user is admin
            return redirect('home') #redirect to home page
    return render(request, 'authentication/login.html') #else redirect to login page again


def logout(request):
    if 'uid' in request.session:
        del request.session['uid'] #remove uid from session variable
    return redirect(login) #redirect to login page

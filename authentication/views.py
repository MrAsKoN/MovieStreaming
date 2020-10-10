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
        return redirect('home')
    return render(request, 'authentication/register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = None
        if (email and password):
            try:
                user = pyfirebase.auth().sign_in_with_email_and_password(email, password)
            except:
                messages.error(request,"Invalid Credentials")
                return render(request, 'authentication/login.html')
            session_id = user['localId']
            request.session['uid'] = session_id
            return redirect('home')
    return render(request, 'authentication/login.html')


def logout(request):
    if 'uid' in request.session:
        del request.session['uid']
    return redirect(login)

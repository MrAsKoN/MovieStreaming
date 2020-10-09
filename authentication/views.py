from django.contrib import messages
from django.shortcuts import render, redirect
from config import pyfirebase, db, auth


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = None
        if not (username and email and password):
            return render(request, 'authentication/register.html')
        try:
            user = auth.create_user(email=email, password=password)
        except:
            messages.error(request, "User Already exists!")
            return render(request, 'authentication/register.html')
        print(user.uid)
        data = {"username": username, "email": email, 'isAdmin': False}
        db.collection('users').document(user.uid).set(data)
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

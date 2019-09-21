from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt

#L_R

def index(request):
    return render(request, "l_r/login_and_registration.html")

def process_login(request, methods=["POST"]):
    if request.POST['form'] == "register":
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            print(pw_hash)
            logged_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            request.session['userid'] = logged_user.id
            return redirect('/dashboard')
    elif request.POST['form'] == "login":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else: 
            user = User.objects.filter(email=request.POST['email'])
            if user: 
                logged_user = user[0]
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['userid'] = logged_user.id
                    return redirect('/dashboard')
                else:
                    errors['password_validate'] = "Password is invalid"
                    for key, value in errors.items():
                        messages.error(request, value)
            else: 
                errors['user_validate'] = "User does not exist"
                for key, value in errors.items():
                    messages.error(request, value)
            return redirect('/')

def logout(request):
    if 'userid' not in request.session:
        return redirect('/')
    del request.session['userid']
    return redirect('/')

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from apps.l_r.models import User
from .models import Trip

#T_B

def dashboard(request):
    if not valid_login(request):
       return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    other_trips = []
    for trip in Trip.objects.all():
        if trip.creator != user:
            other_trips.append(trip)
    context = {
        'first_name' : user.first_name,
        'created_trips' : user.created_trips.all(),
        'joined_trips' : user.joined_trips.all(),
        'other_trips' : other_trips,
    }
    return render(request, "t_b/dashboard.html", context)

def show_trip(request, id):
    if not valid_login(request):
       return redirect('/')
    context = {
        'first_name': User.objects.get(id=request.session['userid']).first_name,
        'trip' : Trip.objects.get(id=id),
    }
    return render (request, "t_b/show_trip.html", context)

def show_create_trip(request):
    if not valid_login(request):
       return redirect('/')
    return render(request, "t_b/create_trip.html")

def process_create_trip(request):
    if not valid_login(request):
       return redirect('/')
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/new')
    else: 
        Trip.objects.create(destination=request.POST['destination'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], plan=request.POST['plan'], creator=User.objects.get(id=request.session['userid']))
        return redirect('/dashboard')

def show_edit_trip(request, id):
    if not valid_login(request):
       return redirect('/')
    context = {
        'first_name': User.objects.get(id=request.session['userid']).first_name,
        'id' : id,
    }
    return render(request, 't_b/edit_trip.html', context)

def process_edit_trip(request, id):
    if not valid_login(request):
       return redirect('/')
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/trips/edit/{id}')
    else:
        trip = Trip.objects.get(id=id)
        trip.destination = request.POST['destination']
        trip.start_date = request.POST['start_date']
        trip.end_date = request.POST['end_date']
        trip.plan = request.POST['plan']
        trip.save()
    return redirect('/dashboard')

def process_remove_trip(request, id):
    if not valid_login(request):
       return redirect('/')
    Trip.objects.get(id=id).delete()
    return redirect('/dashboard')

def process_join_trip(request, id):
    if not valid_login(request):
       return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    Trip.objects.get(id=id).joined_users.add(user)
    return redirect('/dashboard')

def process_cancel_trip(request, id): 
    if not valid_login(request):
       return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    Trip.objects.get(id=id).joined_users.remove(user)
    return redirect('/dashboard')

def valid_login(request):
    if 'userid' in request.session:
       return True
    return False
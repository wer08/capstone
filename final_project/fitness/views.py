import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm, EditForm, RoutineForm
from django.contrib.auth import authenticate, login, logout
from .models import User,Workout, Exercise, Routine
from django.db import IntegrityError
from django.http import JsonResponse
import random


def index(request):
    return render(request, 'index.html')

def diet(request):
    return render(request, 'diet.html')

def exercise(request):
    choice =False
    routine ={}
    if request.method == 'POST':
        form=RoutineForm(request.POST)
        if form.is_valid():
            days = form.cleaned_data['days_per_week']
            gym = form.cleaned_data['gym']
            hypertrophy = form.cleaned_data['hypertrophy']
            weightloss = form.cleaned_data['weightloss']
            if gym and hypertrophy:
                routines_id = Routine.objects.filter(gym = True, hypertrophy = True)
                routine_id = (random.choice(routines_id))
                request.user.routine = routine_id
                request.user.save()
                routine = []
                for training in routine_id.trainings:
                    training_objects = Workout.objects.get(pk = training)
                    training_ids = training_objects.exercises
                    workout=[]
                    for training_id in training_ids:
                        training = Exercise.objects.get(pk = training_id)
                        workout.append(training)
                    routine.append(workout)

                print(routine)
                print("halo")
                choice = True
                return render(request, 'exercise.html',{
                    'form': form,
                    'choice':choice,
                    'routine': routine
                })

    form = RoutineForm()
    return render(request, 'exercise.html',{
        "form": form,
        'choice': choice,
        'routine': routine
    })

def community(request):
    return render(request, 'community.html')

def dashboard(request):
    return render(request,"dashboard.html")

def profile(request,user):
    client = User.objects.get(username = user)
    if request.method == "POST":
        data = request.POST
        picture = request.FILES
        body = json.loads(data.get("body"))
        client.username = body['username']
        client.email = body['email']
        client.calories = body['calories']
        client.carbs = body['carbs']
        client.protein = body['protein']
        client.fat = body['fat']
        client.profile_pic = picture.get("picture")
        client.save()
        return HttpResponse(status = 204)
    else:    
        return JsonResponse(client.serialize())


def profile_view(request,user):
    
    client = User.objects.get(username = user)
    
    form = EditForm(initial={
        'username': client.username,
        'email': client.email,
        'calories': client.calories,
        'carbs': client.carbs,
        'protein': client.protein,
        'fat': client.fat
    })
    return render(request, 'profile.html',{
        'client': client,
        'form': form
    })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, "login.html",{
                    "message": "Invalid username and/or password",
                    'form': form
                })
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirmation =form.cleaned_data['confirm']
            email = form.cleaned_data['email']
            profile_pic = form.cleaned_data['picture']
            # Ensure password matches confirmation
            if password != confirmation:
                return render(request, "register.html", {
                    "message": "Passwords must match."
                })
            # Attempt to create new user
            try:
                client = User.objects.create_user(username, email, password, profile_pic = profile_pic)
                client.save()
            except IntegrityError:
                return render(request, "network/register.html", {
                    "message": "Username already taken."
                })
            login(request, client)
        return HttpResponseRedirect('/')
    else:
        form = RegisterForm()
        return render(request, "register.html", {
            'form': form
        })


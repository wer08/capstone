import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm, EditForm
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.db import IntegrityError
from django.http import JsonResponse


def index(request):
    return render(request, 'index.html')

def profile(request,user):
    client = User.objects.get(username = user)
    if request.method == "PUT":
        data = json.loads(request.body)
        client.username = data['username']
        client.email = data['email']
        client.calories = data['calories']
        client.carbs = data['carbs']
        client.protein = data['protein']
        client.fat = data['fat']
        client.profile_pic = data['profile_pic']
        client.save()
        return HttpResponse(status = 204)
    elif request.method == 'GET':
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


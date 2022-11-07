from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from .models import user
from django.db import IntegrityError


def index(request):
    print("main page")
    return render(request, 'index.html')

def profile_view(request):

    return render(request, 'profile.html',)

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
        print("post method ")
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("valid form")
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
                client = user.objects.create_user(username, email, password, profile_pic)
                client.save()
                print("client saved")
            except IntegrityError:
                return render(request, "network/register.html", {
                    "message": "Username already taken."
                })
            login(request, client)
        else:
            print(form.errors.as_data())
        return HttpResponseRedirect('/')
    else:
        print("get method")
        form = RegisterForm()
        return render(request, "register.html", {
            'form': form
        })


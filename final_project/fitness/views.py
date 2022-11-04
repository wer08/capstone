from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from .models import user
from django.db import IntegrityError


def index(request):
    return render(request, 'index.html')

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
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirmation =form.cleaned_data['confirm_password']
            email = form.cleaned_data['email']
            # Ensure password matches confirmation
            if password != confirmation:
                return render(request, "register.html", {
                    "message": "Passwords must match."
                })
            # Attempt to create new user
            try:
                client = user.objects.create_user(username, email, password)
                client.save()
            except IntegrityError:
                return render(request, "network/register.html", {
                    "message": "Username already taken."
                })
            login(request, client)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


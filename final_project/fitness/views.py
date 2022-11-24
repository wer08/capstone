import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm, EditForm, RoutineForm, PostForm, CommentForm, MealForm, ExerciseForm
from django.contrib.auth import authenticate, login, logout
from .models import User,Workout, Exercise, Routine, Post, Comment, Daily
from django.db import IntegrityError
from django.http import JsonResponse
import random
from django.core.paginator import Paginator
from django.views.generic.edit import FormView
from .forms import GenerateRandomUserForm
from .tasks import create_random_user_accounts
from django.contrib import messages

#function to generate random users. Created to test Celery
class GenerateRandomUserView(FormView):
    template_name = 'generate_random_users.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts.delay(total)
        messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
        return redirect('users_list')

def users_list(request):
    list = User.objects.all()
    return render(request, 'user_list.html',{
        'list': list
    })




def is_ajax(request):

    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"

def daily_calories(request):
    return JsonResponse(request.user.daily_calories, safe=False)

def add_meal(request):
    daily = Daily.objects.get(person = request.user)
    if request.method == 'PUT':
        body = json.loads(request.body)
        calories = body['calories']
        request.user.daily_calories = request.user.daily_calories - int(calories)
        daily.daily_balance.append(-(int(calories)))
        daily.save()
        request.user.save() 
    return HttpResponse(status = 204)

def add_exercise(request):
    daily = Daily.objects.get(person = request.user)

    if request.method == 'PUT':
        body = json.loads(request.body)
        calories = body['calories']
        request.user.daily_calories = request.user.daily_calories + int(calories)
        daily.daily_balance.append((int(calories)))
        daily.save()
        request.user.save()     
    return HttpResponse(status = 204)

def index(request):
    return render(request, 'index.html')

def diet(request):
    return render(request, 'diet.html')

def delete_post(request,post_id):
    if request.method == 'DELETE':
        post = Post.objects.get(pk = post_id)
        post.delete()

    return HttpResponse(status = 204)

def edit_post(request,post_id):
    if request.method == 'PUT':
        post = Post.objects.get(pk = post_id)
        if post.author == request.user:
            data = json.loads(request.body)
            post.body = data['text']
            post.save()
        else:
            return HttpResponse(status = 403)

    return HttpResponse(status = 204)

def exercise(request):
    choice =False
    routine = []
    if request.method == 'POST':
        form=RoutineForm(request.POST)
        if form.is_valid():
            days = form.cleaned_data['days_per_week']
            gym = form.cleaned_data['gym']
            hypertrophy = form.cleaned_data['hypertrophy']
            weightloss = form.cleaned_data['weightloss']

            if gym and hypertrophy:
                routines_id = Routine.objects.filter(gym = True, hypertrophy = True,days_per_week = days)
            elif gym and weightloss:
                routines_id = Routine.objects.filter(gym = True, weightloss = True,days_per_week = days)
            elif (not gym) and hypertrophy:
                routines_id = Routine.objects.filter(gym = False, hypertrophy = True,days_per_week = days)
            elif (not gym) and weightloss:
                routines_id = Routine.objects.filter(gym = False, weightloss = True,days_per_week = days)
                
                try:
                    routine_id = (random.choice(routines_id))
                except IndexError:
                    return render(request, 'error.html',{
                })

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

def comments(request):
    comments = Comment.objects.all()
    comments=[comment.serialize() for comment in comments]
    if request.method == 'POST':
        body = json.loads(request.body)
        text = body['text']
        author = body['author']
        post = body['post']
        author = User.objects.get(username = author)
        post = Post.objects.get(pk = post)
        comment = Comment(body = text, post = post, author=author)
        comment.save()
        return render(request,'_comment.html', {
            'comment': comment
        })
    return JsonResponse(comments, safe=False)

def edit_comment(request, comment_id):
    comment = Comment.objects.get(pk = comment_id)
    if request.method == 'PUT':
        if comment.author == request.user:
            data = json.loads(request.body)
            comment.body = data['body']
            comment.save()
        else:
            return HttpResponse(status = 403)

    return HttpResponse(status = 204)

def delete_comment(request, comment_id):
    if request.method == 'DELETE':
        comment = Comment.objects.get(pk = comment_id)
        comment.delete()
    return HttpResponse(status = 204)


def community(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            author = request.user
            body = form.cleaned_data['body']
            post = Post(author = author, body = body)
            post.save()
            return redirect('community')

    posts = Post.objects.all().order_by('-timestamp')
    comments = Comment.objects.all().order_by('timestamp')
    pagin = Paginator(posts, 5,allow_empty_first_page=False)
    page_number = request.GET.get('page')
    if page_number:
        if int(page_number) > pagin.num_pages:
            page_obj = []
        else:
            page_obj = pagin.get_page(page_number)
    else:
        page_obj = pagin.get_page(page_number)
    form = PostForm()
    if is_ajax(request):
        return render(request, '_posts.html', {
            'posts': page_obj,
            'comments': comments
            })
    return render(request, 'community.html',{
        'posts': page_obj,
        'form': form,
        'comments': comments
    })

def dashboard(request):
    form = MealForm()
    form2 = ExerciseForm()
    try:
        daily = Daily.objects.get(person = request.user)
    except:
        balance = []
        daily = Daily(person = request.user, daily_balance=balance)
        daily.save()

    daily_balance = daily.daily_balance
    return render(request,"dashboard.html",{
        'form': form,
        'form2': form2,
        'daily_balance': daily_balance
    })

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


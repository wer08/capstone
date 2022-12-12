import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm, EditForm, RoutineForm, PostForm, CommentForm, MealForm, ExerciseForm, CaloriesForm
from django.contrib.auth import authenticate, login, logout
from .models import User,Workout, Exercise, Routine, Post, Comment, Daily, Meal, Calendar
from django.db import IntegrityError
from django.http import JsonResponse
import random
from django.core.paginator import Paginator
from django.views.generic.edit import FormView
from django.contrib import messages
import string
from django.utils.crypto import get_random_string
from .functions import add_comments,add_exercises,add_meals,add_posts,add_routines,add_users,add_workouts

def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"

#view to fill the database
def fill_database(request):
    add_users()
    add_posts()
    add_comments()
    add_meals()
    add_exercises()
    add_workouts()
    add_routines()
    users = User.objects.all()
    posts = Post.objects.all()
    comments = Comment.objects.all()
    meals = Meal.objects.all()
    exercises = Exercise.objects.all()
    workouts = Workout.objects.all()
    routines = Routine.objects.all()
    return render(request,'added.html',{
        'users': len(users),
        'posts': len(posts),
        'comments': len(comments),
        'meals': len(meals),
        'exercises': len(exercises),
        'workouts': len(workouts),
        'routines': len(routines)
    })


#view to get data for a chart
def get_data(request,user_id):
    days = {
        0: 'MON',
        1: 'TUE',
        2: "WED",
        3: 'THUR',
        4: 'FRI',
        5: 'SAT',
        6: 'SUN'
    }
    person = User.objects.get(pk = user_id)
    calendars = Calendar.objects.filter(person = person)
    dates = [calendar.date.weekday() for calendar in calendars]
    dates = [days[date] for date in dates]
    dates = dates[-7:]
    dailies = [calendar.day_info for calendar in calendars]
    balances = [calendar.calories_left for calendar in calendars]
    balances = balances[-7:]
    dic = dict(zip(dates,balances))
    return JsonResponse(dic)


#view to change subscription status to subscribed
def subscribe(request):
    if request.method == 'PUT':
        request.user.subscribed = True
        request.user.save()
        return HttpResponse(status=204)

#view to change subscription status to unsubscribed
def unsubscribe(request):
    if request.method == 'PUT':
        request.user.subscribed = False
        request.user.save()
        return HttpResponse(status=204)

#view to change meal(based on request send via Javascript )
def switch_meal(request):
    breakfasts = Meal.objects.filter(type='BR')
    lunches = Meal.objects.filter(type='LU')
    dinners = Meal.objects.filter(type='DIN')
    snacks = Meal.objects.filter(type='SN')

    daily_breakfast = random.choice(breakfasts)
    daily_lunch = random.choice(lunches)
    daily_dinner = random.choice(dinners)
    daily_snack = random.choice(snacks)
    if request.method == 'PUT':
        data = json.loads(request.body)
        daily = Daily.objects.get(person = request.user)
        if data['meal'] == 'breakfast':
            daily.daily_breakfast = daily_breakfast
        elif data['meal'] == 'lunch':
            daily.daily_lunch = daily_lunch
        elif data['meal'] == 'dinner':
            daily.daily_dinner = daily_dinner
        else:
            daily.daily_snack = daily_snack
        daily.save()

    response = {
        'breakfast': daily_breakfast.serialize(),
        'lunch': daily_lunch.serialize(),
        'dinner': daily_dinner.serialize(),
        'snack': daily_snack.serialize()
    }
    return JsonResponse(response)

#view to get current daily calories to update HTML via JS
def daily_calories(request):
    return JsonResponse(request.user.daily_calories, safe=False)

#view to change calory limit
def change_calories(request):
    if request.method == 'PUT':
        body = json.loads(request.body)
        calories = body['calories']
        difference = request.user.calories - int(calories)
        request.user.calories = calories
        request.user.daily_calories -= difference
        request.user.save()
        response = {
            'calories': calories,
            'daily': request.user.daily_calories
        }
        return JsonResponse(response, safe=False)

#view to add meal to daily balance
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

#view to add exercise to daily balance
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

#view to render main page
def index(request):
    return render(request, 'index.html')

#view to render diet page
def diet(request):
    breakfasts = Meal.objects.filter(type='BR')
    lunches = Meal.objects.filter(type='LU')
    dinners = Meal.objects.filter(type='DIN')
    snacks = Meal.objects.filter(type='SN')

    try:
        daily = Daily.objects.get(person = request.user)

    except:
        balance = []
        daily_breakfast = random.choice(breakfasts)
        daily_lunch = random.choice(lunches)
        daily_dinner = random.choice(dinners)
        daily_snack = random.choice(snacks)
        daily = Daily(person = request.user,daily_balance = balance, daily_breakfast = daily_breakfast, daily_lunch = daily_lunch, daily_dinner = daily_dinner, daily_snack = daily_snack)
        daily.save()

    breakfast = daily.daily_breakfast
    lunch = daily.daily_lunch
    dinner = daily.daily_dinner
    snack = daily.daily_snack

    return render(request, 'diet.html',{
        'breakfast': breakfast,
        'lunch': lunch,
        'dinner': dinner,
        'snack': snack
    })

#view to delete post from community page
def delete_post(request,post_id):
    if request.method == 'DELETE':
        post = Post.objects.get(pk = post_id)

        if post.author == request.user:
            post.delete()

    return HttpResponse(status = 204)

#view to edit your posts
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

#view to reset your current training routine
def change_routine(request):
    if request.method == 'PUT':
        request.user.routine = None
        request.user.save()
    return HttpResponse(status = 204)

#view to render exercise page and add a routine
def exercise(request):
    choice =False
    routine = []

    #if user already has a routine this page shows current routine
    if request.user.routine:
        choice = True
        for training in request.user.routine.trainings:
            training_objects = Workout.objects.get(pk = training)
            training_ids = training_objects.exercises
            workout=[]
            for training_id in training_ids:
                training = Exercise.objects.get(pk = training_id)
                workout.append(training)
            routine.append(workout)

    #else it renders a form to get data needed to choose optimal routine
    else:    
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
                elif (not gym) and (not hypertrophy) and (not weightloss):
                    routines_id = Routine.objects.filter(gym = False)
                    
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

    form = RoutineForm()
    return render(request, 'exercise.html',{
        "form": form,
        'choice': choice,
        'routine': routine
    })

#view to add comment to post
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

#view to edit a comment
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

#view to delete comment
def delete_comment(request, comment_id):
    if request.method == 'DELETE':
        comment = Comment.objects.get(pk = comment_id)
        if comment.author == request.user:
            comment.delete()
    return HttpResponse(status = 204)



#view to render community page
def community(request):
    
    #if form is field post is added
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            author = request.user
            body = form.cleaned_data['body']
            post = Post(author = author, body = body)
            post.save()
            return redirect('community')
    
    #else it renders all posts 5 at a time. There is also infinite scroll implementation
    posts = Post.objects.all().order_by('-timestamp')
    comments = Comment.objects.all().order_by('timestamp')
    post_comment = {post.pk: len(Comment.objects.filter(post = post).order_by('timestamp')) for post in posts}
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

    #if request is send via JS it means that user is at the end of page. This renders another 5 posts
    if is_ajax(request):
        return render(request, '_posts.html', {
            'posts': page_obj,
            'comments': comments,
            'post_comment': post_comment
            })
    return render(request, 'community.html',{
        'posts': page_obj,
        'form': form,
        'comments': comments,
        'post_comment': post_comment
    })

#API to get numbers of comments
def get_number_of_comments(request, id):
    posts = Post.objects.all().order_by('-timestamp')
    comments = Comment.objects.all().order_by('timestamp')
    post_comment = {post.pk: len(Comment.objects.filter(post = post).order_by('timestamp')) for post in posts}
    number = post_comment.get(id)
    return JsonResponse(number, safe=False)


#view to render dashboard page
#this page also renders posts made by user that we are currently watching. Infinite scroll is also implemented
def dashboard(request,user_id):
    form = MealForm()
    form2 = ExerciseForm()
    form3 = CaloriesForm()
    user = User.objects.get(pk = user_id)
    try:
        daily = Daily.objects.get(person = user)
    except:
        balance = []
        daily = Daily(person = user, daily_balance=balance)
        daily.save()

    daily_balance = daily.daily_balance
    daily_meals = [meal for meal in daily_balance if meal<0]
    daily_exercise = [exercise for exercise in daily_balance if exercise>0]
    daily_calories = user.daily_calories
    calories = user.calories
    sum_meals = sum(daily_meals)
    sum_exercise = sum(daily_exercise)
    
    posts = Post.objects.filter(author = user).order_by('-timestamp')
    comments = Comment.objects.all().order_by('timestamp')
    post_comment = {post.pk: len(Comment.objects.filter(post = post).order_by('timestamp')) for post in posts}
    pagin = Paginator(posts, 5,allow_empty_first_page=False)
    page_number = request.GET.get('page')
    if page_number:
        if int(page_number) > pagin.num_pages:
            page_obj = []
        else:
            page_obj = pagin.get_page(page_number)
    else:
        page_obj = pagin.get_page(page_number)
    if is_ajax(request):
        print("Rendering new posts")
        return render(request, '_posts.html', {
            'posts': page_obj,
            'comments': comments,
            'post_comment': post_comment
            })
    return render(request,"dashboard.html",{
        'form': form,
        'form2': form2,
        'form3': form3,
        'daily_meals': daily_meals,
        'daily_exercise': daily_exercise,
        'sum_meals': sum_meals,
        'sum_exercise': sum_exercise,
        'posts': page_obj,
        'comments': comments,
        'daily_calories': daily_calories,
        'user_id': user_id,
        'calories': calories,
        'post_comment': post_comment,
    })

#view to change profile informations
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

#view to render profile page
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

#view to render login page
def login_view(request):
    #if method is POST login user
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

#view to logout user
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

#view to register new user
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


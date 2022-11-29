import string
import random
from .models import User,Daily,Meal,Calendar
from django.utils.crypto import get_random_string

from celery import shared_task

@shared_task
def create_random_user_accounts(total):
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
    return '{} random users created with success!'.format(total)

@shared_task
def set_calories_to_zero():
    users = User.objects.all()
    dailys = Daily.objects.all()
    for user in users:
        user.daily_calories = user.calories
        user.save()
    for daily in dailys:
        balance = []
        daily.daily_balance = balance
        daily.save()
    
    print("Calories reseted succesfuly")

@shared_task
def choose_menu():
    breakfasts = Meal.objects.filter(type='BR')
    lunches = Meal.objects.filter(type="LU")
    dinners = Meal.objects.filter(type='DIN')
    snacks = Meal.objects.filter(type="SN")
    breakfast = random.choice(breakfasts)
    lunch = random.choice(lunches)
    dinner = random.choice(dinners)
    snack = random.choice(snacks)
    dailies = Daily.objects.all()
    for daily in dailies:
        daily.daily_breakfast = breakfast
        daily.daily_lunch = lunch
        daily.daily_dinner = dinner
        daily.daily_snack = snack
        daily.save()
    print("Menu refreshed")

@shared_task
def add_to_calendar():
    users = User.objects.all()
    for user in users:
        calendar = Calendar(person = user,day_info = user.daily, calories_left = user.daily_calories)
        calendar.save()
    
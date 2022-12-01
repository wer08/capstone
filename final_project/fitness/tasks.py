
import random
from .models import User,Daily,Meal,Calendar


from celery import shared_task



#task to set calories to chosen value everyday at midnight
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

#task to change meals everyday
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

#task to add daily balance to then show history on graph
@shared_task
def add_to_calendar():
    users = User.objects.all()
    for user in users:
        daily = Daily.objects.get(person = user)
        calendar = Calendar(person = user,day_info = daily, calories_left = user.daily_calories)
        calendar.save()
    
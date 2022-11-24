import string

from .models import User,Daily
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
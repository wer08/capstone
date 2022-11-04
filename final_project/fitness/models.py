from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Sport(models.Model):
    name = models.CharField(max_length=100)
    calories_per_minute = models.IntegerField()


class user(AbstractUser):
    pass
    calories = models.IntegerField()

    
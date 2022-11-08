from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Sport(models.Model):
    name = models.CharField(max_length=100)
    calories_per_minute = models.IntegerField()


class User(AbstractUser):
    pass
    calories = models.IntegerField(default = 2000)
    protein = models.IntegerField(default = 400)
    carbs = models.IntegerField(default = 1000)
    fat = models.IntegerField(default = 600)
    profile_pic = models.ImageField(upload_to='media', default='media/pobrane.png')

    def serialize(self):
        if self.profile_pic:
            return {
                'username': self.username,
                'email': self.email,
                'calories': self.calories,
                'carbs': self.carbs,
                'fat': self.fat,
                'protein': self.protein,
                'profile_pic': self.profile_pic.url

            }
        else:
            return {
                'username': self.username,
                'email': self.email,
                'calories': self.calories,
                'carbs': self.carbs,
                'fat': self.fat,
                'protein': self.protein,
            }

    

class Routine(models.Model):
    days_per_week = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(7)
    ])
    gym = models.BooleanField()
    hypertrophy = models.BooleanField()
    weight_loss = models.BooleanField()

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    target_muscle = models.CharField(max_length=100)
    rounds = models.IntegerField(default=3)
    reps = models.IntegerField(default=8)

class Workout(models.Model):
    exercises = ArrayField(models.IntegerField(), blank = True)

    




    
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Sport(models.Model):
    name = models.CharField(max_length=100)
    calories_per_minute = models.IntegerField()

class Routine(models.Model):
    days_per_week = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(7)
    ])
    gym = models.BooleanField()
    hypertrophy = models.BooleanField()
    weight_loss = models.BooleanField()
    trainings = ArrayField(models.IntegerField(), blank = True) 


class User(AbstractUser):
    pass
    calories = models.IntegerField(default = 2000)
    protein = models.IntegerField(default = 400)
    carbs = models.IntegerField(default = 1000)
    fat = models.IntegerField(default = 600)
    profile_pic = models.ImageField(upload_to='media', default='media/pobrane.png')
    routine = models.ForeignKey(Routine, null=True,on_delete=models.SET_NULL)
    daily_calories = models.IntegerField(default=2000)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.daily_calories = self.calories
        super(User, self).save(*args, **kwargs)




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

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=100)
    comments = ArrayField(models.IntegerField(), null=True)
    timestamp = models.DateTimeField(auto_now=True)
    def serialize(self):
        return {
            'author': self.author.pk,
            'body': self.body,
            'timestamp': self.timestamp
        }

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
            'author': self.author.pk,
            'body': self.body,
            'post': self.post.pk,
            'timestamp': self.timestamp
        }



class Exercise(models.Model):
    name = models.CharField(max_length=100)
    target_muscle = models.CharField(max_length=100)
    rounds = models.IntegerField(default=3)
    reps = models.IntegerField(default=8)

    def __str__(self):
        return f"{self.name}: {self.rounds} rounds. Each round {self.reps} reps."
    
    def serialize(self):
        return {
            'name': self.name,
            'target_muscle': self.target_muscle,
            'rounds': self.rounds,
            'reps': self.reps
        }

class Workout(models.Model):
    name = models.CharField(default="Random workout", max_length=100)
    exercises = ArrayField(models.IntegerField(), blank = True)
    gym = models.BooleanField(default=True)
    hypertrophy = models.BooleanField(default=True)
    weight_loss = models.BooleanField(default=True)
    calories_burned = models.IntegerField(default=500)

    def __str__(self):
        return f"{self.name}    +{self.calories_burned}"




class Meal(models.Model):
    BREAKFAST = 'BR'
    LUNCH = 'LU'
    DINNER = 'DIN'
    SNACK = 'SN'
    MEAL_CHOICES = [
        (BREAKFAST, 'Breakfast'),
        (DINNER, 'Dinner'),
        (LUNCH, 'Lunch'),
        (SNACK, 'Snack'),
    ]
    name = models.CharField(max_length=100)
    calorie = models.IntegerField()
    type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    ingredients = ArrayField(models.CharField(max_length=20),blank=True)
    description = models.CharField(max_length=250)
    

    def __str__(self):
        return f"{self.name}    -{self.calorie}"

class Diet(models.Model):
    first_meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="first_meals")
    second_meal = models.ForeignKey(Meal, on_delete=models.CASCADE,related_name="second_meals")
    third_meal = models.ForeignKey(Meal, on_delete=models.CASCADE,related_name="third_meals")
    snack = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="snacks")

class Daily(models.Model):
    person = models.OneToOneField(User, on_delete=models.CASCADE, related_name="daily")
    daily_balance = ArrayField(models.IntegerField(), null=True)

    


    




    
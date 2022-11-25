from django import forms
from .models import Meal,Workout
from django.core.validators import MinValueValidator, MaxValueValidator

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    username.widget.attrs.update({'class': 'form-control'})

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    confirm = password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    picture = forms.ImageField(required=False)
    picture.widget.attrs.update({'class': 'form-control'})
    username.widget.attrs.update({'class': 'form-control'})

class EditForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    calories = forms.IntegerField()
    carbs = forms.IntegerField()
    protein = forms.IntegerField()
    fat = forms.IntegerField()
    picture = forms.ImageField(required=False)

    picture.widget.attrs.update({'class': 'form-control'})
    username.widget.attrs.update({'class': 'form-control'})
    carbs.widget.attrs.update({'class': 'form-control'})
    calories.widget.attrs.update({'class': 'form-control'})
    protein.widget.attrs.update({'class': 'form-control'})
    fat.widget.attrs.update({'class': 'form-control'})

class RoutineForm(forms.Form):
    days_per_week = forms.IntegerField(min_value=1, max_value=7)
    gym = forms.BooleanField(required=False)
    hypertrophy = forms.BooleanField(required=False)
    weightloss = forms.BooleanField(required=False)
    
    gym.widget.attrs.update({'class': 'form-check-label'})
    hypertrophy.widget.attrs.update({'class': 'form-check-label'})
    weightloss.widget.attrs.update({'class': 'form-check-label'})
    days_per_week.widget.attrs.update({
        'class': 'form-control bg-light mb-1',
        'placeholder': 1
    })

class PostForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control bg-light new_post_area',
        'rows': '3'
    }))

class CommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '3'
    }))

choices_meal = [(meal , f"{meal.name} calories: {meal.calorie}") for meal in Meal.objects.all()]
class MealForm(forms.Form):
    meal = forms.ChoiceField(choices=choices_meal, label='Choose a meal ')
    meal.widget.attrs.update({
        'class': 'form-control mb-2'
    })
    meal_calorie = forms.IntegerField(label="Or just type number of calories ")
    meal_calorie.widget.attrs.update({
        'class': 'form-control mb-2',
        'step': '10',
        'value': '100'
    })

choices_exercise = [(training , f"{training.name} calories: {training.calories_burned}") for training in Workout.objects.all()]
class ExerciseForm(forms.Form):
    training = forms.ChoiceField(choices=choices_exercise, label='Choose a workout ')
    training.widget.attrs.update({
        'class': 'form-control mb-2'
    })
    exercise_calorie = forms.IntegerField(label="Or just type number of calories ")
    exercise_calorie.widget.attrs.update({
        'class': 'form-control mb-2',
        'step': '10',
        'value': '100'
    })

class GenerateRandomUserForm(forms.Form):
    total = forms.IntegerField(
        validators=[
            MinValueValidator(50),
            MaxValueValidator(500)
        ]
    )

class CaloriesForm(forms.Form):
    calories = forms.IntegerField(validators=[MinValueValidator(1000)])

        

  

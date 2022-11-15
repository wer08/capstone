from django import forms

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
        'class': 'form-control bg-light mb-2',
        'placeholder': 1
    })
  

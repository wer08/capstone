from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login_view, name='login'),
    path('logout',views.logout_view, name='logout'),
    path('register',views.register_view, name="register"),
    path('profile/<str:user>',views.profile_view, name='profile'),
    path('profile/edit/<str:user>',views.profile, name="edit_profile"),
    path('exercise',views.exercise, name="exercise")
]


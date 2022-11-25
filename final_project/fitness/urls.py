from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login_view, name='login'),
    path('logout',views.logout_view, name='logout'),
    path('register',views.register_view, name="register"),
    path('profile/<str:user>',views.profile_view, name='profile'),
    path('profile/edit/<str:user>',views.profile, name="edit_profile"),
    path('exercise',views.exercise, name="exercise"),
    path('diet',views.diet, name="diet"),
    path('community',views.community, name="community"),
    path('dashboard/<int:user_id>',views.dashboard, name="dashboard"),
    path('comments',views.comments, name='comments'),
    path('post/delete/<int:post_id>', views.delete_post, name='delete_post'),
    path('post/edit/<int:post_id>', views.edit_post, name='edit_post'),
    path('comment/delete/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('comment/edit/<int:comment_id>', views.edit_comment, name='edit_comment'),
    path('generate',views.GenerateRandomUserView.as_view(), name='generate'),
    path('users_list',views.users_list,name='users_list'),
    path('add_meal', views.add_meal, name='add_meal'),
    path('add_exercise', views.add_exercise, name='add_exercise'),
    path('dashboard/daily_calories', views.daily_calories, name='daily_calories'),
    path('change_calories', views.change_calories, name='change_calories'),
    path('switch_meal',views.switch_meal, name="switch_meal")
]


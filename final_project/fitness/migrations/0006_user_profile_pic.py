# Generated by Django 4.1.3 on 2022-11-07 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0005_exercise_routine_workout_user_carbs_user_fat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='pobrane.png', upload_to='static/profile'),
        ),
    ]

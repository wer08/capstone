from .models import User,Workout, Exercise, Routine, Post, Comment, Daily, Meal, Calendar
import random

def add_users():
    for i in range(25):
        username = f"username{i}"
        password = "1234"
        email = f"username{i}@mail.com"
        user = User(username = username, password = password, email = email)
        user.save()

def add_posts():
    users = User.objects.all()
    for user in users:
        for i in range(8):
            post = Post(author = user, body = f"random post nr{i} made by{user.username}")
            post.save()

def add_comments():
    users = User.objects.all()
    posts = Post.objects.all()
    for post in posts:
        for user in users:
            comment = Comment(author = user, body = f"comment by {user.username}", post = post)
            comment.save()

def add_meals():
    calories = [200,250,300,350,400,500]
    ingredients = ["First ingredient","Second ingredient","Third ingredient","Fourth ingredient"]

    for i in range(10):
        breakfast = Meal(name = f"Breakfast nr{i}", calorie = random.choice(calories),ingredients = ingredients,description = "Here will be directions", type = "BR" )
        lunch = Meal(name = f"Lunch nr{i}", calorie = random.choice(calories),ingredients = ingredients,description = "Here will be directions", type = "LU" )
        dinner = Meal(name = f"Dinner nr{i}", calorie = random.choice(calories),ingredients = ingredients,description = "Here will be directions", type = "DIN" )
        snack = Meal(name = f"Snack nr{i}", calorie = random.choice(calories),ingredients = ingredients,description = "Here will be directions", type = "SN" )
        breakfast.save()
        lunch.save()
        dinner.save()
        snack.save()

def add_exercises():
    for i in range(5):
        chest_exercise_home = Exercise(name = f"Chest Home nr{i}", target_muscle = "Chest", type="Home")
        chest_exercise_gym = Exercise(name = f"Chest Gym nr{i}", target_muscle = "Chest", type="Gym")
        legs_exercise_home = Exercise(name = f"Legs Home nr{i}", target_muscle = "Legs", type="Home")
        legs_exercise_gym = Exercise(name = f"Legs Gym nr{i}", target_muscle = "Legs", type="Gym")
        back_exercise_home = Exercise(name = f"Back Home nr{i}", target_muscle = "Back", type="Home")
        back_exercise_gym = Exercise(name = f"Back Gym nr{i}", target_muscle = "Back", type="Gym")
        biceps_exercise_home = Exercise(name = f"Biceps Home nr{i}", target_muscle = "Biceps", type="Home")
        biceps_exercise_gym = Exercise(name = f"Biceps Gym nr{i}", target_muscle = "Biceps", type="Gym")
        triceps_exercise_home = Exercise(name = f"Triceps Home nr{i}", target_muscle = "Triceps", type="Home")
        triceps_exercise_gym = Exercise(name = f"Triceps Gym nr{i}", target_muscle = "Triceps", type="Gym")
        abs_exercise_home = Exercise(name = f"Abs Home nr{i}", target_muscle = "Abs", type="Home")
        abs_exercise_gym = Exercise(name = f"Abs Gym nr{i}", target_muscle = "Abs", type="Gym")

        chest_exercise_gym.save()
        chest_exercise_home.save()
        legs_exercise_gym.save()
        legs_exercise_home.save()
        back_exercise_gym.save()
        back_exercise_home.save()
        biceps_exercise_gym.save()
        biceps_exercise_home.save()
        triceps_exercise_gym.save()
        triceps_exercise_home.save()
        abs_exercise_gym.save()
        abs_exercise_home.save()

def add_workouts():
    gym_chest = Exercise.objects.filter(type= 'Gym', target_muscle = "Chest")
    gym_legs = Exercise.objects.filter(type= 'Gym', target_muscle = "Legs")
    gym_back = Exercise.objects.filter(type= 'Gym', target_muscle = "Back")
    gym_biceps = Exercise.objects.filter(type= 'Gym', target_muscle = "Biceps")
    gym_triceps = Exercise.objects.filter(type= 'Gym', target_muscle = "Triceps")
    gym_abs = Exercise.objects.filter(type= 'Gym', target_muscle = "Abs")

    home_chest = Exercise.objects.filter(type= 'Home', target_muscle = "Chest")
    home_legs = Exercise.objects.filter(type= 'Home', target_muscle = "Legs")
    home_back = Exercise.objects.filter(type= 'Home', target_muscle = "Back")
    home_biceps = Exercise.objects.filter(type= 'Home', target_muscle = "Biceps")
    home_triceps = Exercise.objects.filter(type= 'Home', target_muscle = "Triceps")
    home_abs = Exercise.objects.filter(type= 'Home', target_muscle = "Abs")

    calories = [500,600,650,700]
    flags = [True, False]
    for i in range(10):
        home_exercises = [random.choice(home_chest).pk, random.choice(home_legs).pk, random.choice(home_back).pk, random.choice(home_biceps).pk, random.choice(home_triceps).pk, random.choice(home_abs).pk]
        gym_exercises = [random.choice(gym_chest).pk, random.choice(gym_legs).pk, random.choice(gym_back).pk, random.choice(gym_biceps).pk, random.choice(gym_triceps).pk, random.choice(gym_abs).pk]

        workout_home = Workout(name= f"Home workout{i}", exercises = home_exercises, gym = False, calories_burned = random.choice(calories), type = "Home", hypertrophy = random.choice(flags), weight_loss = random.choice(flags))
        workout_gym = Workout(name= f"gym workout{i}", exercises = gym_exercises, gym = True, calories_burned = random.choice(calories), type = "Gym", hypertrophy = random.choice(flags), weight_loss = random.choice(flags))

        workout_gym.save()
        workout_home.save()

def add_routines():
    
    for i in range(7):
        for j in range(10):
            flags = [True, False]
            name = f"Routine nr{i}{j}"
            gym_workouts = Workout.objects.filter(gym = True)
            home_workouts = Workout.objects.filter(gym = False)

            gym_trainings = [random.choice(gym_workouts).pk for k in range(i+1)]
            gym_routine = Routine(name=name, days_per_week = i+1, gym = True, hypertrophy = random.choice(flags), weight_loss = random.choice(flags), trainings = gym_trainings )

            home_trainings = [random.choice(home_workouts).pk for k in range(i+1)]
            home_routine = Routine(name=name, days_per_week = i+1, gym = False, hypertrophy = random.choice(flags), weight_loss = random.choice(flags), trainings = home_trainings )

            gym_routine.save()
            home_routine.save()


        

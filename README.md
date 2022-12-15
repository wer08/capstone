# FITNESS APP
#### Video Demo: [Youtube link](https://youtu.be/j7VLovT6m2s)
#### Distinctiveness and Complexity
Complexity: Back-end for the app is build using Django. I have implemented PostgreSQL database using Django models and created multiple APIs to use in JS.
On the front-end side I've used Javascript. Most of the forms are handled by sending request to Django by fetch. It allowed me to render new data without reloading the page. App has multiple event handlers(click, scroll, intersection observer).

Distinctiveness: My app is a whole service that includes creating new menu every day(using celery), creating personal routine, saving data from every day(also celery), displaying charts(chart.js) and many more. All of this required me to learn new things and implement something that I've never created before. One part of it is simillar to previous projects(community tab). I've included it in my project because I believe that it adds to the value of this app. But I've made it different by styling it completely different, not including liking, adding ability to comment.

#### DEV (docker)
1. Listing available containers `docker ps`
2. to enter container `docker exec -it {id} bash`
3. To rebuild container `docker-compose build {name}`
4. to start project's containers `docker-compose up`
5. To start containers without starting the server `docker compose -f 'docker-compose.yml'  -p 'capstone' start`

#### RUNNING

To run this project first build container by typing 'docker-compose build' and next start it with 'docker-compose up'

####FILES

1. media directory where i've stored images used in app.
2. requirements.txt: where all the packages are listed(they're installed when container is build)
3. DOCKERFILE: File needed to build docker container
4. docker-compose.yml: Specification of all the services that are gonna be build
5. final_project/celery.py: Specification of celery and task schedule
6. fitness/views.py: All django views
7. fitness/urls.py: All needed urls
8. fitness/tasks.py: definitions of celery tasks
9. fitness/models.py: models for postgreSQL
10. fitness/functions.py: functions to populate database
11. fitness/forms.py: forms used in this project
12. fitness/admin.py: registering models to admin page
13. fitness/templatetags/fitness_extras.py: registering additional tags 
14. fitness/templates/_comment.html: html for one comment
15. fitness/templates/_post.html: html for one post
16. fitness/templates/_posts.html: html for all posts
17. fitness/templates/added.html: html to show results of populating database
18. fitness/templates/community.html: html for community tab
19. fitness/templates/dashboard.html: html for dashboard tab
20. fitness/templates/diet.html: html for diet tab
21. fitness/templates/error.html: html to render error message when there is no routine available
22. fitness/templates/exercise.html: html for exercise page
23. fitness/templates/generate_random_user.html: html for a page to test celery
24. fitness/templates/index.html: html for main page
25. fitness/templates/layout.html: html with layout for all pages
26. fitness/templates/login.html: html with login form
27. fitness/templates/profile.html: html for profile page
28. fitness/templates/register.html: html with register form
29. fitness/templates/test_chart.html: html dor testing charts
30. fitness/templates/user_list.html: html to display list of users(also testing celery)
31. fitness/static/script.js: Javascript for this app
32. fitness/static/styles.css: CSS for this app


#### Description:

My project is a fitness web applicatipn. It's a django application. Main features that I implemented are:
- Database using PostreSQL
- Community page which is simmilar to facebook page
- Exercise page
- Diet page
- Dashboard page
- editing your profile


##### Database
I created a database with 9 tables(using Django models:
- Routine
- User
- Post
- Comment
- Exercise
- Workout
- Meal
- Daily
- Calendar

###### Routine

Routine table contains couple of fields. Routine name, days_per_week(value from one to seven), gym(Boolean field), hypertrophy(boolean field), weight_loss(boolean field), trainings(Array field with workouts id)

###### User

Every user has username, password, email (fields provided by Django) and additional fields:
- calories(amount of daily calories)
- protein(amount of daily protein)
- carbs(amount of daily carbs)
- fat(amount of daily fat)
- profile_pic(image field with default picture if user don't want to upload a picture)
- routine(Routine that is chosen for you based on your preference)
- daily_calories(current daily balance)
- subscribed(boolean field)

###### Post

This table contains 4 columns. Author(User), body(CharField), comments(ArrayField with id's of comments), timestamp(DateTimeField)

###### Comment

Comment table has 4 columns:
- Author(User)
- body(charField)
- post(Post)
- timestamp(DateTimeField)

###### Exercise

There are 5 columns in this table. Name(CharField), target_muscle(CharField from EXERCISE_CHOICES), rounds(IntegerField), reps(IntegerField), type(CharField[gym or home])

###### Workout

This table contains:
- name(CharField)
- exercises(ArrayField with id of Exercise)
- gym(BooleanField)
- hypertrophy(BooleanField)
- weight_loss(BooleanField)
- calories_burned(IntegerField)
- type(CharField[gym or home]

###### Daily

This table contains:
- person(User)
- daily_balance(ArrayField with calories burned from exercise and calories provided from meals)
- daily_lunch(Meal)
- daily_breakfast(Meal)
- daily_dinner(Meal)
- daily_snack(Meal)


###### Meal

This table contains:
- name(charField)
- calorie(IntegerField)
- type(CharField[from MEAL_CHOICES])
- ingredients(ArrayField)
- description(CharField)

###### Calendar

This table contains:
- person(User)
- date(DateField)
- day_info(Daily)
- calories_left(Integer Field that keeps track of how many calories user can spare for a day)





##### HTML&CSS

###### Layout
Whole project is build using bootstrap. In layout file (layout.html) are parts of each page that are the same. This includes navigation bar that have couple of links:
- link to Home Page
- link to Exercise Page if you are logged in
- link to Diet Page if you are logged in
- link to Community Page if you are logged in
- link to Dashboard Page if you are logged in
- link to register if you're not logged in
- link to log in if you're not already
- link to log out if you're logged in
- link to edit your profile if you are logged in

It also includes footer with links to my facebook, instagram, twitter 

###### Main Page
On Main Page(index.html) we are able to see picture and links to all the other pages. I chose a layout where there is a picture on one sie and text with link on other.
I also chose to animate each entry when it appears on screen.

###### Profile Page

On this page(profile.html) we can see our profile info(username, e-mail,calories, protein, carbs, fat and profile picture).When we press Edit button we form appears where we can change any of this information 

###### Exercise Page 

On Exercise page(exercise.html) we can see 2 things:
- If user doesn't have a routine there will be form displayed. This form is displayed one question at a time. When user answers all the questions routine is chosen for him
- If user has a routine there will be displayed workout plan for every training day

###### Diet Page

On diet page(diet.html) we see a menu chosen for that day for user. If user don't like the dish there is a switch button

###### Profil

On user profile page(profil.html) user can see a form to change every data that he enetered during registration as well as ability to choose profile picture from his computer

###### login

This Page(login.html) contains a single form that prompts the user to enter his username and password

###### register

Registration page(register.html) contains a single form with several inputs:
- username
- email adress
- Password
- Confirmation password

###### Community

On community page(community.html) We see a form to add a post at the top. Below there are posts already published. Each post in an animated div ( '_post.html' )._
If user is an author of a post he has the ability to edit or delete it.
Inside the post div there are divs with comments(_comment.html)_ that are made visible by clicking the all Comments button or comment button(which opens a form to add a comment).
If you are an author of a comment you have the ability to delete or edit it.

We see 5 posts at a time and the is an infinite scroll feature implemented.

###### Dashboard

On Dashboard page we can see how many calories we have left for a day. there are 2 buttons at the top of the page: one to add a meal to daily balance and one to add exercise to daily balance.
Below we can change our calorie goal for a day.
below that there is a table with calories eaten or burned.
On the next div there is a chart which shows how many calories we had left in last 7 days.
Under the chart user can see all the posts that he had posted(the same as in the community page)

##### Javascript(script.js)

In this project I've heavilly used fetching API build in Django to make sure all the data is displayed as soon as button is clicked not after refreshing. I've also use fetch with PUT, POST and DELETE method to handle editing, adding and deleting posts and comments in community and dashboard page

###### Infinite Scroll
I've implemented inifnite scroll to community and dashboard page. To do that I've used django pagination but instead of a button I used fetch in javascript when user is reaching end of page

###### Chart
In dashboard page I've created chart to show user calorie balance in last week. I've build it using chart.js 
 
##### Python and Django

###### Celery

To set up celery I've created 2 files:
- celery.py in which I've set up 3 scheduled tasks:
 - setting daily calories to chosen value
 - refreshing all the meals 
 - adding daily balance to calendar
 
- tasks.py in this file I've implemented the task that are used in schedule.

###### urls.py

This is the file that contains urls to all the views

###### models.py

In this file I've defined models for database. More detail about this is in Database paragraph. I've added serialize function to a couple of models(The ones that I need to send through JSON

###### templatetags/fitness_extras.py

In this file I've created a tag to get vsalue from dictionary in template

###### functions.py

This file contains function definition to functions that populate database

###### views.py

I've created multiple views:
- fill_database view. It uses functions defined in fucntions.py and renders page with information about created fields
- get_data is the view to get information used in chart(in dashboard page)
- subscribe change the subscribed status of current user to True
- Unsubscribe change the subscribed status of current user to False
- switch_meal changes the meal in Diet page and save it to daily object linked to current user and sends JSON with new meal
- daily_calories returns JSON with daily_calories
- change_calories this view changes the value of calories and daily_calories of logged user
- add_meal changes daily_balance and daily_calories
- add_exercise The same as add_meal but for exercise
- index renders the main page
- diet creates daily field for this user in it's not already created and renders diet page with meals chosen for that dat with random.choice() function
- delete_post deletes post
- edit_post get data from fetch method in JS and saves the changes using PUT method
- change_routine It changes routine field for user to None
- exercise this view does to things. If user already has routine it renders the page with it. If not it renders a form to choose routine
- comments This view uses data send by fetch to add comment to database
- edit_comment uses data send by fetch to edit an entry in database to edit comment
- delete_comment deletes comment
- community if form is field it adds a post otherwise it renders the posts using pagination. There is a check in this page to check if request for more posts was send by ajax. If that's a case it renders more posts(see [Infinite Scroll](https://github.com/wer08/capstone/blob/master/README.md#infinite-scroll))
- get_number_of_comments API to get number of comments on post
- dashboard This page also creates daily isntance if it's not created already. Otherwise it renders dashboard page with posts made by current user as in community page
- profile changes the profile data
- profile_view renders profile page
- login_view renders login page and if method is POST logs the user
- logout_view it logouts and redirects to index page
- register_view if form is submitted it register new user otherwise it renders empty form
###### Docker

To set up Docker we need 3 files:
- Dockerfile: It have the description of actions that need to be done when docker is build. Most importantly to install everything from requirements.txt
- requirements.txt In this file I've listed all packages that need to be installed
- docker-compose.yml it defines services that I use in my docker-compose:
 - postgres db
 - rabbitmq(to set up celery)
 - celery
 - celery-beat







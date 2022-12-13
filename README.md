# FITNESS APP
#### Video Demo:  https://youtu.be/Y7FheTaGx3Q
#### Description:
##### OVERVIEW

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
 
##### Python and flask(app.py)

###### Configuration

First of all I needed to configure 4 things:
- Connection to database
- Session
- Stripe payment client
- Mail client using mailtrap

###### Route ("/")

On this route I configured backside of a main page. All this route is practically doing is execute some queries to get data from database and give it to html.
It also prompts flash message when there are no flights on the chosen date

###### Route ("/buy")

This route renders buy.html. It GETs data from index.html and gives it back to buy.html to show the price

On the Post method it renders charge.html.

###### Route ("/charge")

 This route does 3 things. It computes payment using stripe. It sends a confirmation e-mail to the user who bought the ticket and it adds a record to booked table in database. When It's all done it redirects the user to his booked flights page

###### Route ("/bought")

This route gets all the flights from the booked table that logged in user bought. Than it gets details from other tables and renders a page with list of booked flights

###### Route ("/profil")

Get method of this route gets all the current data from user table and sends it to render a page with them as initial value.
Post method updates the database with new (after validation) information.

###### Route ("/logut")

It clears the session and shows flash message informing about logging out

###### Route ("/login")

GET methos renders a login.html page

POST method is validating entered data, creating session variables and showing flash messages according to situation

###### Route ("/upload")

This is the route resposible for uploading users profile picture and confirming the change with flash message

###### Route ("/register")

This route does a couple of things. First it renders register.html. Next it gets Inputed data and validate it on server side.
If everything is correct it adds an entry to users table, sends confirmation e-mail and show informing flash message







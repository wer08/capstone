function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

document.addEventListener("DOMContentLoaded", function () {
  /* Adding events to community page is in function because it has to be run after more posts are added using infinity scroll*/
  try {
    addEventsToCommunity();
  } catch (e) {
    console.error(e, e.stack);
  }

  /*Adding events to dashboard page */
  try {
    addEventsToDashboard();
  } catch (e) {
    console.error(e, e.stack);
  }

  /*Adding events to diet page */
  try {
    addEventsToDiet();
  } catch (e) {
    console.error(e, e.stack);
  }



  try {
    form_edit = document.querySelector("#editing");
    form_edit.style.display = "none";
    client_info = document.querySelector("#info");
    client_info.style.display = "block";
    edit_button = document.querySelector("#edit");
    edit_button.addEventListener("click", show_form);
    save_button = document.querySelector("#save");
    save_button.addEventListener("click", info);
  } catch (TypeError) {
    console.log("not profile page");
  }

  try {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("revealed");
        } else {
          entry.target.classList.remove("revealed");
        }
      });
    });
    var reveals = document.querySelectorAll(".reveal");
    var ups = document.querySelectorAll('.up');
    ups.forEach((el)=>observer.observe(el));
    reveals.forEach((el) => observer.observe(el));
  } catch (TypeError) {
    console.log(`not a main page`);
  }

  try{
    document.querySelector(`#change_routine`).addEventListener("click", change_routine);
  }
  catch(e)
  {
    console.error(e,e.stack);
  }

  try {
    days = document.querySelector("#days_per_week");
    days.style.display = "block";
    gym = document.querySelector("#gym");
    gym.style.display = "none";
    hypertrophy = document.querySelector("#hypertrophy");
    hypertrophy.style.display = "none";
    weightloss = document.querySelector("#weightloss");
    weightloss.style.display = "none";

    document
      .querySelector("#days_per_week_button")
      .addEventListener("click", () => {
        days.style.display = "none";
        gym.style.display = "block";
      });

    document.querySelector("#gym_button").addEventListener("click", () => {
      gym.style.display = "none";
      hypertrophy.style.display = "block";
    });

    document
      .querySelector("#hypertrophy_button")
      .addEventListener("click", () => {
        hypertrophy.style.display = "none";
        weightloss.style.display = "block";
        document.querySelector(`#final`).disabled = false;
      });


  } 
  catch (e) {
    console.error(e, e.stack);
  }

  let prevScrollpos = window.pageYOffset;
  window.onscroll = () => {
    let currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
      document.querySelector(".navbar").style.top = "0";
    } else {
      document.querySelector(".navbar").style.top = "-50px";
    }
    prevScrollpos = currentScrollPos;
  };

  loadings = document.querySelectorAll(".loading");
  loadings.forEach((loading) => (loading.style.display = "none"));

  if (this.body.classList.contains("community")) {
    let counter = 1;
    window.addEventListener("scroll", () => {
      element = document.querySelector("#posts");
      if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        fetch(`/community?page=${counter + 1}`, {
          headers: {
            "X-Requested-With": "XMLHttpRequest",
          },
        })
          .then((response) => response.text())
          .then((body) => {
            loadings = document.querySelectorAll(".loading");
            loadings.forEach((loading) => (loading.style.display = "block"));
            setTimeout(() => {
              element.innerHTML += body;
              addEventsToCommunity();
              loadings = document.querySelectorAll(".loading");
              loadings.forEach((loading) => (loading.style.display = "none"));
            }, 1500);
            counter++;
          });
      }
    });
  } else if (this.body.classList.contains("dashboard_page")) {
    let counter = 1;
    window.addEventListener("scroll", () => {
      element = document.querySelector("#posts-dashboard");
      console.log(`${window.innerHeight + window.scrollY +1} >= ${document.body.offsetHeight}`);
      if (window.innerHeight + window.scrollY +1>= document.body.offsetHeight) {
        console.log(`?page=${counter + 1}`);
        fetch(`?page=${counter + 1}`, {
          headers: {
            "X-Requested-With": "XMLHttpRequest",
          },
        })
          .then((response) => response.text())
          .then((body) => {
            console.log(body);
            loadings = document.querySelectorAll(".loading");
            loadings.forEach((loading) => (loading.style.display = "block"));
            setTimeout(() => {
              element.innerHTML += body;
              addEventsToCommunity();
              loadings = document.querySelectorAll(".loading");
              loadings.forEach((loading) => (loading.style.display = "none"));
            }, 1500);
            counter++;
          });
      }
    });
  }

  try{
    printChart();
  } catch(e){
    console.error(e, e.stack)
  }

});

function addEventsToDashboard() {
  meal_button = document.querySelector("#add_meal");
  meal_button.addEventListener("click", show_meal_choice);

  exercise_button = document.querySelector("#add_exercise");
  exercise_button.addEventListener("click", show_exercise_choice);

  cancel_meal_button = document.querySelector("#cancel_meal");
  cancel_meal_button.addEventListener("click", cancel_meal_choice);

  cancel_exercise_button = document.querySelector("#cancel_exercise");
  cancel_exercise_button.addEventListener("click", cancel_exercise_choice);

  add_meal_button = document.querySelector("#meal_button-id_meal");
  add_meal_button.addEventListener("click", add_meal);

  add_meal_calorie_button = document.querySelector(
    "#meal_button-id_meal_calorie"
  );
  add_meal_calorie_button.addEventListener("click", add_meal_calorie);

  add_exercise_training_button = document.querySelector(
    "#exercise_button-id_training"
  );
  add_exercise_training_button.addEventListener("click", add_exercise_training);

  add_exercise_calorie_button = document.querySelector(
    "#exercise_button-id_exercise_calorie"
  );
  add_exercise_calorie_button.addEventListener("click", add_exercise_calorie);

  change_calories_button = document.querySelector("#change_calories_link");
  change_calories_button.addEventListener("click", change_calories);

  cancel_calories_button = document.querySelector("#cancel_calories");
  cancel_calories_button.addEventListener("click", cancel_calories);

  save_calories_button = document.querySelector("#change_calories_button");
  save_calories_button.addEventListener("click", save_calories);
}

function addEventsToCommunity() {
  fetch(`/comments`)
    .then((response) => response.json())
    .then((comments) => {
      comments.forEach((comment) => edit(comment));
    });

  close_comment_buttons = document.querySelectorAll(".close_comment");
  close_comment_buttons.forEach((button) => {
    let id = button.id;
    button.addEventListener("click", close_comment);
    button.myParam = id;
  });

  add_comment_buttons = document.querySelectorAll(".add_comment");
  add_comment_buttons.forEach((button) => {
    let id = button.id;
    button.addEventListener("click", show_add_comment);
    button.myParam = id;
  });

  save_comment_buttons = document.querySelectorAll(".save_button");
  save_comment_buttons.forEach((button) => {
    let id = button.id;
    button.addEventListener("click", save_comment);
    button.myParam = id;
  });

  comments = document.querySelectorAll(".comments");
  comments.forEach((comment) => (comment.style.display = "none"));

  show_comments = document.querySelectorAll(".show_comments");
  show_comments.forEach((show_comment) => {
    let id = show_comment.id;
    show_comment.addEventListener("click", show_comments_func);
    show_comment.myParam = id;
  });

  delete_post_buttons = document.querySelectorAll(".delete_post");
  delete_post_buttons.forEach((delete_post_button) => {
    let id = delete_post_button.id;
    delete_post_button.addEventListener("click", delete_post);
    delete_post_button.myParam = id;
  });

  edit_post_buttons = document.querySelectorAll(".edit_post");
  edit_post_buttons.forEach((edit_post_button) => {
    let id = edit_post_button.id;
    edit_post_button.addEventListener("click", edit_post);
    edit_post_button.myParam = id;
  });

  cancel_post_edit_buttons = document.querySelectorAll(".cancel_post_edit");
  cancel_post_edit_buttons.forEach((cancel_post_edit_button) => {
    let id = cancel_post_edit_button.id;
    cancel_post_edit_button.addEventListener("click", cancel_edit_post);
    cancel_post_edit_button.myParam = id;
  });

  save_post_edit_buttons = document.querySelectorAll(".save_post_edit_button");
  save_post_edit_buttons.forEach((save_post_edit_button) => {
    let id = save_post_edit_button.id;
    save_post_edit_button.addEventListener("click", save_post_edit);
    save_post_edit_button.myParam = id;
  });

  delete_comment_buttons = document.querySelectorAll(".delete_comment");
  delete_comment_buttons.forEach((delete_comment_button) => {
    let id = delete_comment_button.id;
    delete_comment_button.addEventListener("click", delete_comment);
    delete_comment_button.myParam = id;
  });

  edit_comment_buttons = document.querySelectorAll(".edit_comment");
  edit_comment_buttons.forEach((edit_comment_button) => {
    let id = edit_comment_button.id;
    edit_comment_button.addEventListener("click", edit_comment);
    edit_comment_button.myParam = id;
  });

  cancel_comment_edit_buttons = document.querySelectorAll(
    ".cancel_comment_edit"
  );
  cancel_comment_edit_buttons.forEach((cancel_comment_edit_button) => {
    let id = cancel_comment_edit_button.id;
    cancel_comment_edit_button.addEventListener("click", cancel_comment_edit);
    cancel_comment_edit_button.myParam = id;
  });

  save_comment_edit_buttons = document.querySelectorAll(".save_comment_edit");
  save_comment_edit_buttons.forEach((save_comment_edit_button) => {
    let id = save_comment_edit_button.id;
    save_comment_edit_button.addEventListener("click", save_comment_edit);
    save_comment_edit_button.myParam = id;
  });
}

function addEventsToDiet() {
  switch_breakfast_button = document.querySelector("#switch_breakfast");
  switch_breakfast_button.addEventListener("click", switch_breakfast);

  switch_lunch_button = document.querySelector("#switch_lunch");
  switch_lunch_button.addEventListener("click", switch_lunch);

  switch_dinner_button = document.querySelector("#switch_dinner");
  switch_dinner_button.addEventListener("click", switch_dinner);

  switch_snack_button = document.querySelector("#switch_snack");
  switch_snack_button.addEventListener("click", switch_snack);
}

function printChart(){
  fetch('get_data')
  .then(response => response.json())
  .then(dict => {
    
    const ctx = document.getElementById('chart');
    Chart.defaults.font.size = 14;
    Chart.defaults.color = "#000000";

    new Chart(ctx, {
      type: 'line',
      data: {
        datasets: [{
          label: 'Daily Calories left',
          data: dict,
          borderWidth: 3,
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  })

}

function change_routine(){
    const request = new Request(`change_routine`, {
        headers: { "X-CSRFToken": csrftoken },
      });
      console.log("change routine");
      fetch(request, {
        method: "PUT",
        mode: "same-origin",
      })
      .then(()=>{
        window.location.href = 'exercise';
      })

}

function switch_breakfast() {
  const request = new Request(`switch_meal`, {
    headers: { "X-CSRFToken": csrftoken },
  });
  breakfast_name = document.querySelector(`#breakfast_name`);
  breakfast_ingredients = document.querySelector(`#breakfast_ingredients`);
  breakfast_description = document.querySelector(`#breakfast_description`);
  fetch(request, {
    method: "PUT",
    mode: "same-origin",
    body: JSON.stringify({
      meal: "breakfast",
    }),
  })
    .then((response) => response.json())
    .then((meals) => {
      breakfast = meals.breakfast;
      breakfast_name.innerHTML = breakfast.name;
      breakfast_description.innerHTML = breakfast.description;
      breakfast_ingredients.innerHTML = "";
      breakfast.ingredients.forEach((ingredient) => {
        li = document.createElement("li");
        li.classList.add("text-light");
        li.innerHTML = ingredient;
        breakfast_ingredients.appendChild(li);
      });

      console.log(breakfast);
    });
  console.log("switch breakfst");
}

function switch_lunch() {
  const request = new Request(`switch_meal`, {
    headers: { "X-CSRFToken": csrftoken },
  });
  lunch_name = document.querySelector(`#lunch_name`);
  lunch_ingredients = document.querySelector(`#lunch_ingredients`);
  lunch_description = document.querySelector(`#lunch_description`);
  fetch(request, {
    method: "PUT",
    mode: "same-origin",
    body: JSON.stringify({
      meal: "lunch",
    }),
  })
    .then((response) => response.json())
    .then((meals) => {
      lunch = meals.lunch;
      lunch_name.innerHTML = lunch.name;
      lunch_description.innerHTML = lunch.description;
      lunch_ingredients.innerHTML = "";
      lunch.ingredients.forEach((ingredient) => {
        li = document.createElement("li");
        li.classList.add("text-light");
        li.innerHTML = ingredient;
        lunch_ingredients.appendChild(li);
      });
    });
  console.log("switch lunch");
}

function switch_dinner() {
  const request = new Request(`switch_meal`, {
    headers: { "X-CSRFToken": csrftoken },
  });
  dinner_name = document.querySelector(`#dinner_name`);
  dinner_ingredients = document.querySelector(`#dinner_ingredients`);
  dinner_description = document.querySelector(`#dinner_description`);
  fetch(request, {
    method: "PUT",
    mode: "same-origin",
    body: JSON.stringify({
      meal: "dinner",
    }),
  })
    .then((response) => response.json())
    .then((meals) => {
      dinner = meals.dinner;
      dinner_name.innerHTML = dinner.name;
      dinner_description.innerHTML = dinner.description;
      dinner_ingredients.innerHTML = "";
      dinner.ingredients.forEach((ingredient) => {
        li = document.createElement("li");
        li.classList.add("text-light");
        li.innerHTML = ingredient;
        dinner_ingredients.appendChild(li);
      });
    });
  console.log("switch dinner");
}

function switch_snack() {
  const request = new Request(`switch_meal`, {
    headers: { "X-CSRFToken": csrftoken },
  });
  snack_name = document.querySelector(`#snack_name`);
  snack_ingredients = document.querySelector(`#snack_ingredients`);
  snack_description = document.querySelector(`#snack_description`);
  fetch(request, {
    method: "PUT",
    mode: "same-origin",
    body: JSON.stringify({
      meal: "snack",
    }),
  })
    .then((response) => response.json())
    .then((meals) => {
      snack = meals.snack;
      snack_name.innerHTML = snack.name;
      snack_description.innerHTML = snack.description;
      snack_ingredients.innerHTML = "";
      snack.ingredients.forEach((ingredient) => {
        li = document.createElement("li");
        li.classList.add("text-light");
        li.innerHTML = ingredient;
        snack_ingredients.appendChild(li);
      });
    });
  console.log("switch snack");
}

function save_calories() {
  const request = new Request(`/change_calories`, {
    headers: { "X-CSRFToken": csrftoken },
  });

  calories = document.querySelector("#id_calories").value;

  fetch(request, {
    method: "PUT",
    mode: "same-origin",
    body: JSON.stringify({
      calories: calories,
    }),
  })
    .then((response) => response.json())
    .then((calories_json) => {
      remaining_calories = document.querySelector("#remaining_calories");
      remaining_calories.innerHTML = calories_json.daily;
      main_page = document.querySelector("#dashboard");
      main_page.classList.remove("dashboard");

      change_calories_view = document.querySelector("#change_calories");
      change_calories_view.style.display = "none";

      daily_limit = document.querySelector("#daily-limit");
      daily_limit.innerHTML = `Daily Limit: ${calories_json.calories}`;
    });
}

function change_calories() {
  main_page = document.querySelector("#dashboard");
  main_page.classList.add("dashboard");

  change_calories_view = document.querySelector("#change_calories");
  change_calories_view.style.display = "block";
  change_calories_view.pointerEvents = "auto";
}

function cancel_calories() {
  main_page = document.querySelector("#dashboard");
  main_page.classList.remove("dashboard");

  change_calories_view = document.querySelector("#change_calories");
  change_calories_view.style.display = "none";
}

function add_meal() {
  main_page = document.querySelector("#dashboard");
  main_page.classList.remove("dashboard");

  meal_choice = document.querySelector("#meal");
  meal_choice.style.display = "none";

  list = document.querySelector("#calorie-balance-meals");
  meal = document.querySelector("#id_meal").value;
  meal = meal.split("-");
  meal = meal[1];
  li = document.createElement("li");
  li.classList.add("list-group-item", "bg-transparent");
  list.appendChild(li);
  li.innerHTML = `<strong>-${meal}<strong>`;
  const request = new Request(`/add_meal`, {
    headers: { "X-CSRFToken": csrftoken },
  });

  fetch(request, {
    method: "PUT",
    mode: "same-origin",
    body: JSON.stringify({
      calories: meal,
    }),
  }).then(() => {
    remaining_calories = document.querySelector("#remaining_calories");
    fetch("daily_calories")
      .then((response) => response.json())
      .then((daily_calories) => {
        remaining_calories.innerHTML = daily_calories;
        if (daily_calories < 0) {
          remaining_calories.classList.add("text-danger");
          remaining_calories.classList.remove("text-success");
        }
      });
  });
}

function add_meal_calorie() {
  main_page = document.querySelector("#dashboard");
  main_page.classList.remove("dashboard");

  meal_choice = document.querySelector("#meal");
  meal_choice.style.display = "none";

  list = document.querySelector("#calorie-balance-meals");
  calories = document.querySelector("#id_meal_calorie");
  li = document.createElement("li");
  li.classList.add("list-group-item", "bg-transparent");
  list.appendChild(li);
  li.innerHTML = `-${calories.value}`;

  const request = new Request(`/add_meal`, {
    headers: { "X-CSRFToken": csrftoken },
  });

  fetch(request, {
    method: "PUT",
    mode: "same-origin",
    body: JSON.stringify({
      calories: calories.value,
    }),
  }).then(() => {
    remaining_calories = document.querySelector("#remaining_calories");
    fetch("daily_calories")
      .then((response) => response.json())
      .then((daily_calories) => {
        remaining_calories.innerHTML = daily_calories;
        if (daily_calories < 0) {
          remaining_calories.classList.add("text-danger");
          remaining_calories.classList.remove("text-success");
        }
      });
  });
}

function add_exercise_training() {
  main_page = document.querySelector("#dashboard");
  main_page.classList.remove("dashboard");

  exercise_choice = document.querySelector("#exercise");
  exercise_choice.style.display = "none";

  list = document.querySelector("#calorie-balance-exercise");
  training = document.querySelector("#id_training").value;
  training = training.split("+");
  training = training[1];
  li = document.createElement("li");
  li.classList.add("list-group-item", "bg-transparent");
  list.appendChild(li);
  li.innerHTML = `${training}`;

  const request = new Request(`/add_exercise`, {
    headers: { "X-CSRFToken": csrftoken },
  });

  fetch(request, {
    method: "PUT",
    mode: "same-origin",
    body: JSON.stringify({
      calories: training,
    }),
  }).then(() => {
    remaining_calories = document.querySelector("#remaining_calories");
    fetch("daily_calories")
      .then((response) => response.json())
      .then((daily_calories) => {
        remaining_calories.innerHTML = daily_calories;
        if (daily_calories >= 0) {
          remaining_calories.classList.add("text-success");
          remaining_calories.classList.remove("text-danger");
        }
      });
  });
}

function add_exercise_calorie() {
  main_page = document.querySelector("#dashboard");
  main_page.classList.remove("dashboard");

  exercise_choice = document.querySelector("#exercise");
  exercise_choice.style.display = "none";

  list = document.querySelector("#calorie-balance-exercise");
  training = document.querySelector("#id_exercise_calorie");
  li = document.createElement("li");
  li.classList.add("list-group-item", "bg-transparent");
  list.appendChild(li);
  li.innerHTML = `${training.value}`;

  const request = new Request(`/add_exercise`, {
    headers: { "X-CSRFToken": csrftoken },
  });

  fetch(request, {
    method: "PUT",
    mode: "same-origin",
    body: JSON.stringify({
      calories: training.value,
    }),
  }).then(() => {
    remaining_calories = document.querySelector("#remaining_calories");
    fetch("daily_calories")
      .then((response) => response.json())
      .then((daily_calories) => {
        remaining_calories.innerHTML = daily_calories;
        if (daily_calories >= 0) {
          remaining_calories.classList.add("text-success");
          remaining_calories.classList.remove("text-danger");
        }
      });
  });
}

function show_meal_choice(evt) {
  main_page = document.querySelector("#dashboard");
  main_page.classList.add("dashboard");

  meal_choice = document.querySelector("#meal");
  meal_choice.style.display = "block";
  meal_choice.style.pointerEvents = "auto";
}

function cancel_meal_choice(evt) {
  main_page = document.querySelector("#dashboard");
  main_page.classList.remove("dashboard");

  meal_choice = document.querySelector("#meal");
  meal_choice.style.display = "none";
}

function show_exercise_choice(evt) {
  main_page = document.querySelector("#dashboard");
  main_page.classList.add("dashboard");

  exercise_choice = document.querySelector("#exercise");
  exercise_choice.style.display = "block";
  exercise_choice.style.pointerEvents = "auto";
}

function cancel_exercise_choice(evt) {
  main_page = document.querySelector("#dashboard");
  main_page.classList.remove("dashboard");

  exercise_choice = document.querySelector("#exercise");
  exercise_choice.style.display = "none";
}

function save_comment_edit(evt) {
  let id = evt.currentTarget.myParam;
  id = id.split("-");
  id = id[1];
  body = document.querySelector(`#edit_comment_area-${id}`).value;
  console.log(body);

  const request = new Request(`/comment/edit/${id}`, {
    headers: { "X-CSRFToken": csrftoken },
  });
  fetch(request, {
    method: "PUT",
    mode: "same-origin",
    body: JSON.stringify({
      body: body,
    }),
  }).then(() => {
    comment_body = document.querySelector(`#comment_body-${id}`);
    comment_body.innerHTML = body;
    comment_body.style.display = "block";
    document.querySelector(`#comment_edit-${id}`).style.display = "none";
  });
}

function cancel_comment_edit(evt) {
  let id = evt.currentTarget.myParam;
  id = id.split("-");
  id = id[1];
  comment_body = document.querySelector(`#comment_body-${id}`);
  comment_body.style.display = "block";
  comment_textarea = document.querySelector(`#comment_edit-${id}`);
  comment_textarea.style.display = "none";
}

function edit_comment(evt) {
  let id = evt.currentTarget.myParam;
  id = id.split("-");
  id = id[1];
  comment_body = document.querySelector(`#comment_body-${id}`);
  comment_body.style.display = "none";
  comment_textarea = document.querySelector(`#comment_edit-${id}`);
  comment_textarea.style.display = "block";
  document.querySelector(`#edit_comment_area-${id}`).value =
    comment_body.innerHTML.replace(/<[^>]*>/g, "");
}

function delete_comment(evt) {
  let id = evt.currentTarget.myParam;
  id = id.split("-");
  id = id[1];
  const request = new Request(`/comment/delete/${id}`, {
    headers: { "X-CSRFToken": csrftoken },
  });

  fetch(request, {
    method: "DELETE",
  }).then(() => {
    comment = document.querySelector(`#comment-${id}`);
    comment.remove();
    console.log("Comment deleted");
  });
}

function save_post_edit(evt) {
  let id = evt.currentTarget.myParam;
  id = id.split("-");
  id = id[1];
  new_post_body = document.querySelector(`#edit_post_area-${id}`).value;
  console.log(new_post_body);
  post_text = document.querySelector(`#post_text-${id}`);

  console.log("edit button clicked");

  const request = new Request(`/post/edit/${id}`, {
    headers: { "X-CSRFToken": csrftoken },
  });

  fetch(request, {
    method: "PUT",
    mode: "same-origin",
    body: JSON.stringify({
      text: new_post_body,
    }),
  }).then(() => {
    post_text.innerHTML = new_post_body;
    document.querySelector(`#post_textarea-${id}`).style.display = "none";
    post_text.style.display = "block";
  });
}

function cancel_edit_post(evt) {
  let id = evt.currentTarget.myParam;
  id = id.split("-");
  id = id[1];
  post_textarea = document.querySelector(`#post_textarea-${id}`);
  post_textarea.style.display = "none";
  post_text = document.querySelector(`#post_text-${id}`);
  post_text.style.display = "block";
}

function edit_post(evt) {
  let id = evt.currentTarget.myParam;
  id = id.split("-");
  id = id[1];
  post_text = document.querySelector(`#post_text-${id}`);
  console.log(post_text.innerHTML);
  post_text.style.display = "none";
  post_textarea = document.querySelector(`#post_textarea-${id}`);
  post_textarea.style.display = "block";
  document.querySelector(`#edit_post_area-${id}`).value =
    post_text.innerHTML.replace(/<[^>]*>/g, "");
}

function delete_post(evt) {
  let id = evt.currentTarget.myParam;
  id = id.split("-");
  id = id[1];
  post = document.querySelector(`#post-${id}`);
  const request = new Request(`/post/delete/${id}`, {
    headers: { "X-CSRFToken": csrftoken },
  });
  fetch(request, {
    method: "DELETE",
  }).then(() => {
    console.log("running animation");
    post.classList.add("deleted");
    setTimeout(() => {
      post.remove();
    }, 500);
  });
}

function show_comments_func(evt) {
  let id = evt.currentTarget.myParam;
  id = id.split("-");
  id_post = id[1];
  comments = document.querySelector(`#comments-${id_post}`);
  if (comments.style.display == "none") {
    comments.style.display = "block";
  } else {
    comments.style.display = "none";
  }
}

function save_comment(evt) {
  let id = evt.currentTarget.myParam;
  id = id.split("_");
  id_post = id[1];
  text = document.querySelector(`#text-area_${id_post}`).value;

  const username = JSON.parse(document.getElementById("username").textContent);

  const request = new Request(`/comments`, {
    headers: { "X-CSRFToken": csrftoken },
  });

  fetch(request, {
    method: "POST",
    mode: "same-origin",
    body: JSON.stringify({
      text: text,
      post: id_post,
      author: username,
    }),
  })
    .then((response) => response.text())
    .then((body) => {
      document.querySelector(`#comment-text${id_post}`).style.display = "none";
      console.log("I'm here");
      console.log(body);

      const div = document.querySelector(`#comments-${id_post}`);
      const newDiv = document.createElement("div");
      newDiv.innerHTML = body;
      div.appendChild(newDiv);
    });
}

function close_comment(evt) {
  let id = evt.currentTarget.myParam;
  let query = `#comment-${id}`;
  document.querySelector(query).style.display = "none";
}

function show_add_comment(evt) {
  let id = evt.currentTarget.myParam;
  let query = `#comment-text${id}`;
  document.querySelector(query).style.display = "block";
  comments = document.querySelector(`#comments-${id}`);
  comments.style.display = "block";
}

function edit() {
  console.log("editing");
}

function show_form() {
  form_edit.style.display = "block";
  client_info.style.display = "none";
}

function info(evt) {
  const username = JSON.parse(document.getElementById("username").textContent);
  const request = new Request(`/profile/edit/${username}`, {
    headers: { "X-CSRFToken": csrftoken },
  });

  new_username = document.querySelector(`#id_username`).value;
  email = document.querySelector(`#id_email`).value;
  calories = document.querySelector(`#id_calories`).value;
  carbs = document.querySelector(`#id_carbs`).value;
  protein = document.querySelector(`#id_protein`).value;
  fat = document.querySelector(`#id_fat`).value;
  picture = document.querySelector(`#id_picture`).files[0];

  json_body = JSON.stringify({
    username: new_username,
    email: email,
    calories: calories,
    carbs: carbs,
    protein: protein,
    fat: fat,
  });

  formData = new FormData();
  formData.append("picture", picture);
  formData.append("body", json_body);
  formData.append("test", "test");

  fetch(request, {
    method: "POST",
    mode: "same-origin",
    body: formData,
  })
    .then(() => fetch(`/profile/edit/${username}`))
    .then((response) => response.json())
    .then((client) => {
      document.querySelector("#username_info").innerHTML = client.username;
      document.querySelector("#email").innerHTML = client.email;
      document.querySelector("#calories").innerHTML = `${client.calories} cal`;
      document.querySelector("#carbs").innerHTML = `${client.carbs} cal`;
      document.querySelector("#protein").innerHTML = `${client.protein} cal`;
      document.querySelector("#fat").innerHTML = `${client.fat} cal`;
      if (client.profile_pic) {
        document.querySelector("#profile_pic").src = client.profile_pic;
      } else {
        document.querySelector("#profile_pic").src = "/media/media/pobrane.png";
      }
      form_edit.style.display = "none";
      client_info.style.display = "block";
    });

  evt.preventDefault();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');



document.addEventListener('DOMContentLoaded',function(){
    try{
        form_edit = document.querySelector('#editing');
        form_edit.style.display = 'none';
        client_info = document.querySelector('#info');
        client_info.style.display = 'block';
        edit_button = document.querySelector('#edit');
        edit_button.addEventListener('click',show_form)
        save_button = document.querySelector("#save");
        save_button.addEventListener('click',info);

    } catch (TypeError)
    {
        console.log("not profile page");
    }

    try{
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting){
                    entry.target.classList.add('revealed');
                }
                else{
                    entry.target.classList.remove('revealed');
                }   
            })
        })
        var reveals = document.querySelectorAll(".reveal");
        reveals.forEach((el) => observer.observe(el));
    }
    catch(TypeError){
        console.log(`not a main page`);
    }

    try{
        days = document.querySelector('#days_per_week');
        days.style.display = 'block';
        gym = document.querySelector('#gym');
        gym.style.display ='none';
        hypertrophy = document.querySelector('#hypertrophy');
        hypertrophy.style.display = 'none';
        weightloss = document.querySelector('#weightloss');
        weightloss.style.display ='none';

        document.querySelector('#days_per_week_button').addEventListener('click',()=>{
            days.style.display = 'none';
            gym.style.display= 'block';
        })

        document.querySelector('#gym_button').addEventListener('click',()=>{
            gym.style.display = 'none';
            hypertrophy.style.display= 'block';
        })
        
        document.querySelector('#hypertrophy_button').addEventListener('click',()=>{
            hypertrophy.style.display = 'none';
            weightloss.style.display= 'block';
        })

    }
    catch(e){
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

    loading = document.querySelector('#loading');
    loading.style.display = 'none';
    
    /* Adding events to community page is in function because it has to be run after more posts are added using infinity scroll*/
    addEventsToCommunity();



    if(this.body.classList.contains('community'))
    {
        let counter = 1;
        window.addEventListener('scroll',()=>{
            element = document.querySelector("#posts");
            if((window.innerHeight + window.scrollY) >= document.body.offsetHeight)
            {
                fetch(`/community?page=${counter+1}`,{
                    headers:{
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                })
                .then(response => response.text())
                .then(body => {
                    loading.style.display = 'block';                   
                    setTimeout(()=>{
                        element.innerHTML += body;
                        addEventsToCommunity();
                        loading.style.display = 'none';
                    },1500)
                    counter ++;
                })
            }
        })
    }

  
});

function addEventsToCommunity()
{
    fetch(`/comments`)
        .then(response => response.json())
        .then(comments => {
            comments.forEach(comment => edit(comment));
        })

    close_comment_buttons = document.querySelectorAll('.close_comment');
    close_comment_buttons.forEach(button => {
        let id = button.id;
        button.addEventListener('click',close_comment)
        button.myParam = id;
    })

    add_comment_buttons = document.querySelectorAll('.add_comment');
    add_comment_buttons.forEach(button => {
        let id = button.id;
        button.addEventListener('click',show_add_comment);
        button.myParam = id;
    })

    save_comment_buttons = document.querySelectorAll('.save_button');
    save_comment_buttons.forEach(button => {
        let id = button.id;
        button.addEventListener('click',save_comment);
        button.myParam = id;
    })

    comments = document.querySelectorAll('.comments');
    comments.forEach(comment => comment.style.display = 'none');


    show_comments = document.querySelectorAll('.show_comments');
    show_comments.forEach(show_comment => {
        let id = show_comment.id;
        show_comment.addEventListener('click',show_comments_func);
        show_comment.myParam = id;
    })

    delete_post_buttons = document.querySelectorAll('.delete_post');
    delete_post_buttons.forEach(delete_post_button => {
        let id = delete_post_button.id;
        delete_post_button.addEventListener('click',delete_post);
        delete_post_button.myParam = id;
    })

    edit_post_buttons = document.querySelectorAll('.edit_post');
    edit_post_buttons.forEach(edit_post_button => {
        let id = edit_post_button.id;
        edit_post_button.addEventListener('click',edit_post);
        edit_post_button.myParam = id;
    })

    cancel_post_edit_buttons = document.querySelectorAll('.cancel_post_edit');
    cancel_post_edit_buttons.forEach(cancel_post_edit_button => {
        let id = cancel_post_edit_button.id;
        cancel_post_edit_button.addEventListener('click',cancel_edit_post);
        cancel_post_edit_button.myParam = id;
    })

}

function cancel_edit_post(evt)
{
    let id = evt.currentTarget.myParam;
    id = id.split("-");
    id = id[1];
    post_textarea = document.querySelector(`#post_textarea-${id}`);
    post_textarea.style.display = 'none'; 
    post_text = document.querySelector(`#post_text-${id}`);
    post_text.style.display = 'block';
    
}

function edit_post(evt)
{
    let id = evt.currentTarget.myParam;
    id = id.split("-");
    id = id[1];
    post_text = document.querySelector(`#post_text-${id}`);
    post_text.style.display = 'none';
    post_textarea = document.querySelector(`#post_textarea-${id}`);
    post_textarea.style.display = 'block'; 
    document.querySelector(`#edit_post_area-${id}`).value = post_text.innerHTML;
    console.log('editing');
}

function delete_post(evt)
{
    let id = evt.currentTarget.myParam;
    id = id.split("-");
    id = id[1];
    post = document.querySelector(`#post-${id}`);
    console.log(`#post-${id}`);
    const request = new Request(
        `/post/delete/${id}`,
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request,{
        method: 'DELETE',
    })
    .then(() => {
        post.remove();
        console.log('post removed');
    })
}


function show_comments_func(evt)
{
    let id = evt.currentTarget.myParam;
    id = id.split("-");
    id_post = id[1];
    comments = document.querySelector(`#comments-${id_post}`);
    if(comments.style.display == 'none')
    {
        comments.style.display = 'block';
    }
    else
    {
        comments.style.display = 'none';
    }
 
}

function save_comment(evt)
{
    let id = evt.currentTarget.myParam;
    id = id.split("_");
    id_post = id[1];
    text = document.querySelector(`#text-area_${id_post}`).value;

    const username = JSON.parse(document.getElementById('username').textContent);

    const request = new Request(
        `/comments`,
        {headers: {'X-CSRFToken': csrftoken}}
    );
    
    fetch(request,{
        method: 'POST',
        mode: "same-origin",
        body: JSON.stringify({
            text: text,
            post: id_post,
            author: username
        })
    })
    .then(() => {
        document.querySelector(`#comment-text${id_post}`).style.display ='none';
        const div = document.querySelector(`#comments-${id_post}`);
        const newDiv = document.createElement("div");
        newDiv.classList.add('container', 'w-100', 'bg-light', 'rounded', 'pt-2');
        newDiv.innerHTML = `<h6>${username}</h6> <p>${text}</p>`
        div.appendChild(newDiv);

    });
}

function close_comment(evt)
{
    let id = evt.currentTarget.myParam;
    let query = `#comment-${id}`;
    document.querySelector(query).style.display ='none';
}

function show_add_comment(evt)
{
    let id = evt.currentTarget.myParam;
    let query = `#comment-text${id}`;
    document.querySelector(query).style.display ='block';
    comments = document.querySelector(`#comments-${id}`);
    comments.style.display = 'block';

}


function edit(){
    console.log('editing')
}


function show_form(){
    form_edit.style.display = 'block';
    client_info.style.display = 'none';
}

function info(evt){
    const username = JSON.parse(document.getElementById('username').textContent);
    const request = new Request(
        `/profile/edit/${username}`,
        {headers: {'X-CSRFToken': csrftoken}}
    );
    
    new_username = document.querySelector(`#id_username`).value;
    email = document.querySelector(`#id_email`).value;
    calories = document.querySelector(`#id_calories`).value;
    carbs = document.querySelector(`#id_carbs`).value;
    protein = document.querySelector(`#id_protein`).value;
    fat = document.querySelector(`#id_fat`).value;
    picture = document.querySelector(`#id_picture`).files[0]

    json_body = JSON.stringify({
        username: new_username,
        email: email,
        calories: calories,
        carbs: carbs,
        protein: protein,
        fat: fat,
    })

    formData = new FormData()
    formData.append("picture",picture);
    formData.append("body",json_body);
    formData.append("test","test");

    fetch(request,{
        method: 'POST',
        mode: "same-origin",
        body: formData
    })
    .then(() => 
        fetch(`/profile/edit/${username}`))
        .then(response => response.json())
        .then(client => {
            document.querySelector('#username_info').innerHTML = client.username;
            document.querySelector('#email').innerHTML = client.email;
            document.querySelector('#calories').innerHTML = `${client.calories} cal`;
            document.querySelector('#carbs').innerHTML = `${client.carbs} cal`;
            document.querySelector('#protein').innerHTML = `${client.protein} cal`;
            document.querySelector('#fat').innerHTML = `${client.fat} cal`;
            if(client.profile_pic)
            {
                document.querySelector('#profile_pic').src = client.profile_pic;
            }
            else
            {
                document.querySelector("#profile_pic").src = "/media/media/pobrane.png";
            }
            form_edit.style.display = 'none';
            client_info.style.display = 'block';
        })
    
    evt.preventDefault();
}




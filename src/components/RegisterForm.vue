<script setup> 

import { ref, onMounted, toRefs } from 'vue';
let csrf_token = ref("");


let successMessage = ref("");
let errorMessage = ref([]);

let profilePic = ref(null);

const state = toRefs({ profilePic, csrf_token, successMessage, errorMessage });

function getCsrfToken(){
    fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            csrf_token.value = data.csrf_token;
        })
}

onMounted(() => {
    getCsrfToken();
});

function createUser()  {
    let form = document.querySelector("#post-form");
    let formData = new FormData(form);

    const confirmpassword = formData.get('confirmpassword');
    const password = formData.get('password');
    const email = formData.get('email');
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

    let errors = [];

    if (!email || email.trim() === '') {
        errors.push('Error in Email field - This field is required.');
    } else if (!emailPattern.test(email)) {
        errors.push('Error in Email field - Please enter a valid email address.');
    }

    if (!password || password.trim() === ''){
        errors.push('Error in Password field - This field is required.');
    } else if (!passwordPattern.test(password)) {
        errors.push('Error in Password field - Password must be at least 8 characters long and contain at least one letter and one number.');
    }
    if (confirmpassword != password){
        errors.push('Error in Confirm Password field - Passwords do not match.');
    }

    if (errors.length > 0) {
        errorMessage.value = errors;
        return;
    }

    console.log(Array.from(formData.entries()));


    fetch("/api/v1/users/register", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrf_token.value,
        }
    })
    .then((response) => {
        if (response.ok) {
            return response.json();
        } else {
            throw response;
        }
    })
    .then((data) => {
        successMessage.value = "Account successfully created!";
        errorMessage.value = [];
        console.log(data);
    })
    .catch((error) => {
        error.json().then((data) => {
            if (data.errors) {
                errorMessage.value = data.errors;
            } else {
                errorMessage.value = ["An unexpected error occurred."];
            }
            successMessage.value = "";
            console.log(data);
        });
    });

};


</script>

<template>
    <form @submit.prevent="createUser" id="registration" method="post" class = "form">
        <div class="alert alert-success" v-if="successMessage">{{ successMessage }}</div>
    
        <div v-if="errorMessage.length">
          <div class="alert alert-danger" v-for="(error, index) in errorMessage" :key="index">
            {{ error }}
          </div>
        </div>
        
        <div class="form-group mb-3">
            <label for="email" class="form-label">Email</label>
            <input type="email" name="email" class="form-control" />
        </div>

        <div class="form-group mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" name="password" class="form-control" />
        </div>

        <div class="form-group mb-3">
            <label for="confirmpassword" class="form-label">Confirm Password</label>
            <input type="confirmpassword" name="confirmpassword" class="form-control" />
        </div>
        
       
        <button type="submit" class="btn btn-success">Register</button>
    
    </form>
    
</template>
    
<style>
.form{
    position: absolute;
    top: 150px;
    left: 35%;
    border: 1px solid #ccc;
    padding: 20px;
    width: 500px;
    margin: 0 auto;
    background-color: white;
    border-radius: 5px;
}

body{
    background-color: rgb(251, 233, 203);
}

h2{
    position: absolute;
    top: 108px;
    left: 475px;

}
button{
    width: 100%;

}

input[type="file"] {
    background-color: #f1f1f1;
    border: 1px solid #ccc;
    color: #333;
    font-size: 16px;
    padding: 10px;
}

</style>
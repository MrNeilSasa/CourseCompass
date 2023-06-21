<script setup>
import {ref, onMounted} from 'vue'
import RegisterForm from '../components/RegisterForm.vue';

let register = ref([])

</script>

<template>
    <div>
        <h1>Register</h1>
        <RegisterForm />
    </div>
</template>

<style>
h1{
    text-align: center;
    left: 35%;
    font-size: 30px;
}
</style>
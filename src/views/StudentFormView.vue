<script setup>
import { ref } from "vue";
import StudentForm from '../components/StudentForm.vue';

let student = ref([])
</script>

<template>

  <div class="text-center">
    <h1>Student Form</h1>
    <StudentForm />
  </div>
  
</template>

<style>
/* Add any component specific styles here */



</style>
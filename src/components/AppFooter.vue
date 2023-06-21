<template>
      <footer class="text-center">
          <div class="">
              <p>Copyright &copy {{ year }} Virtual Solutions.</p>
          </div>
      </footer>
</template>

<script setup>
import { ref } from "vue";

const year = (new Date).getFullYear();
</script>

<style>
/* Add any component specific styles here */
</style>
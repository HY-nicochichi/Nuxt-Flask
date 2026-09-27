<script setup lang="ts">
  import 'bootstrap/dist/js/bootstrap.bundle.min.js'
  import NavBar from '~/components/NavBar.vue'
</script>


<template>
  <NuxtLoadingIndicator color="deeppink" :height="5"/>
  <header class="pt-3">
    <NavBar/>
  </header>
  <main class="p-3">
    <NuxtPage/>
  </main>
</template>


<style>
  body {
    background-color: var(--color-bg);
    color: var(--color-text);
  }
</style>

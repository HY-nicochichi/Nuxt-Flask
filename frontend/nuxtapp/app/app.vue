<script setup lang="ts">
  import NavBar from '~/components/NavBar.vue'
</script>


<template>
  <div class="bg-black text-white min-vh-100">
    <NuxtLoadingIndicator
      color="deeppink" :height="5"
    />
    <NavBar/>
    <div class="p-3">
      <NuxtPage/>
    </div>
  </div>
</template>

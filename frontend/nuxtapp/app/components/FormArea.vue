<template>
  <form class="col-sm-9 col-md-7 col-lg-5 bg-primary bg-opacity-25 p-3">
    <slot/>
  </form>
</template>

 
<style scoped>
  form {
    border-style: solid;
    border-width: 2px;
    border-radius: 0.5rem;
    border-color: var(--color-text);
  }
</style>

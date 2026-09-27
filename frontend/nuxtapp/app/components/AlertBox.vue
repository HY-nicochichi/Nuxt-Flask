<script setup lang="ts">
  import {useAlertStore} from '~/stores'

  const alert = useAlertStore()
</script>


<template>
  <aside v-if="alert.value.show" role="alert" class="bg-danger bg-opacity-50 mb-3 p-2">
    ※ {{ alert.value.msg }}
  </aside>
</template>


<style scoped>
  aside {
    border-style: solid;
    border-width: 1.5px;
    border-radius: 0.25rem;
    border-color: var(--color-text);
  }
</style>

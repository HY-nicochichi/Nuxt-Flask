<script setup lang="ts">
  import {useAlertStore} from '~/stores'

  const alert = useAlertStore()
</script>


<template>
  <div v-if="alert.value.show" class="bg-danger bg-opacity-50 border border-danger rounded mb-3 px-3 py-2">
    ※ {{ alert.value.msg }}
  </div>
</template>

<script setup lang="ts">
  import {useAlertStore} from '~/stores/AlertStore'

  const alert = useAlertStore()
  alert.value = {show: false, msg: ''}
</script>


<template>
  <div v-if="alert.value.show" class="alert alert-danger mb-3" role="alert">
    ※ {{ alert.value.msg }}
  </div>
</template>

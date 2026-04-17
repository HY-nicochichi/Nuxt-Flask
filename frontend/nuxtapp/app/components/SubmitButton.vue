<script setup lang="ts">
  import {LoadingSpinner} from '~/components/SvgIcons'

  const props = defineProps<{
    invalid: boolean, submitting: boolean, click: () => Promise<void>
  }>()
</script>


<template>
  <button class="btn btn-primary" :disabled="invalid || submitting" @click="click">
    <LoadingSpinner
      v-if="submitting" class="mx-2" :size="'25'" :color="'white'"
    />
    <span v-else>submit</span>
  </button>
</template>

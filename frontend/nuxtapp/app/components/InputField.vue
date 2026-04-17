<script setup lang="ts">
  const props = defineProps<{label: string, type: string}>()
  const value = defineModel<string>({required: true})
</script>


<template>
  <div class="mb-4">
    <label class="mb-2">{{ props.label }}</label>
    <input :type="props.type" v-model="value" class="form-control"/>
  </div>
</template>

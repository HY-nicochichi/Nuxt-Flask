<script setup lang="ts">
  const props = defineProps({
    inputs: {type: Array<Input>, required: true}
  })

  const isDisabled: ComputedRef<boolean> = computed(() =>
    props.inputs.some(input => !input.validation(input.value))
  )

  const emit = defineEmits(['update', 'submit'])
</script>

<template>
  <div class="col-sm-9 col-md-7 col-lg-5 border border-primary bg-light p-3">
    <div v-for="(input, index) in inputs" class="mb-4">
      <label class="mb-2">{{ input.label }}</label>
      <input
        class="form-control border border-primary"
        v-bind:type="input.type"
        v-bind:value="input.value"
        v-on:input="emit('update', index, ($event.target as HTMLInputElement).value)"
      />
    </div>
    <br>
    <div>
      <button
        class="btn btn-primary"
        v-bind:disabled="isDisabled"
        v-on:click="emit('submit')"
      >
        submit
      </button>
    </div>
  </div>
</template>

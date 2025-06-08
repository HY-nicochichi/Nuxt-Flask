<script setup lang="ts">
  import {LoadingSpinner} from '~/components/SvgIcons'
  import type {Input} from '~/types'

  const props = defineProps({
    inputs: {type: Array<Input>, required: true}
  })

  const invalid: ComputedRef<boolean> = computed(() =>
    props.inputs.some(input => !input.validation(input.value))
  )
  const submitting: Ref<boolean> = ref(false)

  const emit = defineEmits(['update', 'submit'])

  async function submit(): Promise<void> {
    submitting.value = true
    emit('submit', () => {
      submitting.value = false
    })
  }
</script>


<template>
  <div class="col-sm-9 col-md-7 col-lg-5 bg-white bg-opacity-25 border border-white rounded p-3">
    <div v-for="(input, index) in inputs" class="mb-4">
      <label class="mb-2">{{ input.label }}</label>
      <input
        class="form-control"
        :type="input.type"
        :value="input.value"
        @input="emit('update', index, ($event.target as HTMLInputElement).value)"
      />
    </div>
    <br>
    <div>
      <button
        class="btn btn-primary"
        :disabled="invalid || submitting"
        @click="submit"
      >
        <LoadingSpinner
          v-if="submitting" class="mx-2"
          :size="'25'" :color="'white'"
        />
        <span v-else>submit</span>
      </button>
    </div>
  </div>
</template>

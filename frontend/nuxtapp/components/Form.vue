<script setup lang="ts">
  defineProps<{inputs: Input[], submit: Submit}>()
</script>

<template>
  <div class="col-sm-9 col-md-7 col-lg-5 border border-primary bg-light p-3">
    <div v-for="input of inputs" class="mb-4">
      <label class="mb-2">{{ input.label.value }}</label>
      <input v-bind:type="input.type.value" class="form-control border border-primary" v-model="input.model.value"/>
    </div>
    <br>
    <div>
      <button class="btn btn-primary" v-on:click="submit.func">{{ submit.name }}</button>
    </div>
  </div>
</template>

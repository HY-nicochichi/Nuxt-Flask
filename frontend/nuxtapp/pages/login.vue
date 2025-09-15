<script setup lang="ts">
  useHead({title: 'login'})

  const inputValues: Ref<string[]> = ref(['', ''])

  function setInputValue(index: number, value: string): void {
    inputValues.value[index] = value
  }

  const inputs: ComputedRef<Input[]> = computed(() => [
    {
      label: 'email',
      type: 'text',
      value: inputValues.value[0],
      validation: validateEmail
    },
    {
      label: 'password',
      type: 'password',
      value: inputValues.value[1],
      validation: validatePassword
    }
  ])

  async function tryLogin(): Promise<void> {
    const resp: Resp = await accessJwtPost(
      inputs.value[0].value, inputs.value[1].value
    )
    if (resp.status === 200) {
      setJwt(resp.body.access_token)
      useRouter().push({name: 'index'})
    }
    else {
      useAlertStore().showMessage(resp.body.msg)
    }
  }
</script>

<template>
  <AlertBox/>
  <h4 class="fw-bolder mb-3">login</h4>
  <BasicForm
    v-bind:inputs="inputs"
    v-on:update="setInputValue"
    v-on:submit="tryLogin"
  />
</template>

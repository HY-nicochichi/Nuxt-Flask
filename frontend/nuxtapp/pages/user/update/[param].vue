<script setup lang="ts">
import { accessUserPatch } from '~/composables/ApiClient'

  const param: string = useRoute().params.param as string ?? ''

  if (!['email', 'password', 'name'].includes(param)) {
    useRouter().push('/404')
  }

  useHead({title: 'update ' + param})

  const type: string = param === 'password' ? 'password' : 'text'

  const inputValues: Ref<string[]> = ref(['', ''])

  function setInputValue(index: number, value: string): void {
    inputValues.value[index] = value
  }

  const inputs: ComputedRef<Input[]> = computed(() => [
    {
      label: 'current ' + param,
      type: type,
      value: inputValues.value[0],
      validation: selectValidation(param)
    },
    {
      label: 'new ' + param,
      type: type,
      value: inputValues.value[1],
      validation: selectValidation(param)
    }
  ])

  async function tryUpdateUser(): Promise<void> {
    const resp: Resp = await accessUserPatch(
      param, inputs.value[0].value, inputs.value[1].value
    )
    if (resp.status === 200) {
      useRouter().push({name: 'user-info'})
    }
    else {
      useAlertStore().showMessage(resp.body.msg)
    }
  }
</script>

<template>
  <AlertBox/>
  <h4 class="fw-bolder mb-3">update {{ param }}</h4>
  <BasicForm
    v-bind:inputs="inputs"
    v-on:update="setInputValue"
    v-on:submit="tryUpdateUser"
  />
</template>

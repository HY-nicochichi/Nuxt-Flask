<script setup lang="ts">
  import AlertBox from '~/components/AlertBox.vue'
  import BasicForm from '~/components/BasicForm.vue'
  import {accessJwtPost, accessUserPost} from '~/composables/ApiClient'
  import {setJwt} from '~/composables/JwtManager'
  import {validateEmail, validateName, validatePassword} from '~/composables/Validation'
  import {useAlertStore} from '~/stores'
  import type {Input, Resp} from '~/types'

  useHead({title: 'new user'})

  const router = useRouter()
  const alert = useAlertStore()

  const inputValues: Ref<string[]> = ref(['', '', ''])

  function setInputValue(index: number, value: string): void {
    inputValues.value[index] = value
  }

  const inputs: ComputedRef<Input[]> = computed(() => [
    {
      label: 'email',
      type: 'text',
      value: inputValues.value[0] ?? '',
      validation: validateEmail
    },
    {
      label: 'password',
      type: 'password',
      value: inputValues.value[1] ?? '',
      validation: validatePassword
    },
    {
      label: 'name',
      type: 'text',
      value: inputValues.value[2] ?? '',
      validation: validateName
    }
  ])

  async function createUser(done: () => void): Promise<void> {
    const resp1: Resp = await accessUserPost(
      inputs.value[0]?.value ?? '', inputs.value[1]?.value ?? '', inputs.value[2]?.value ?? ''
    )
    if (resp1.status === 201) {
      const resp2: Resp = await accessJwtPost(
        inputs.value[0]?.value ?? '', inputs.value[1]?.value ?? ''
      )
      setJwt(resp2.body.access_token)
      router.push({name: 'index'})
    }
    else {
      alert.show(resp1.body.msg)
      done()
    }
  }
</script>


<template>
  <AlertBox/>
  <h4 class="fw-bolder mb-3">new user</h4>
  <BasicForm
    :inputs="inputs"
    @update="setInputValue"
    @submit="createUser"
  />
</template>

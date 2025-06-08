<script setup lang="ts">
  import AlertBox from '~/components/AlertBox.vue'
  import BasicForm from '~/components/BasicForm.vue'
  import {accessJwtPost} from '~/composables/ApiClient'
  import {setJwt} from '~/composables/JwtManager'
  import {validateEmail, validatePassword} from '~/composables/Validation'
  import {useAlertStore} from '~/stores'
  import type {Input, Resp} from '~/types'

  useHead({title: 'login'})

  const router = useRouter()
  const alert = useAlertStore()

  const inputValues: Ref<string[]> = ref(['', ''])

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
    }
  ])

  async function login(done: () => void): Promise<void> {
    const resp: Resp = await accessJwtPost(
      inputs.value[0]?.value ?? '', inputs.value[1]?.value ?? ''
    )
    if (resp.status === 200) {
      setJwt(resp.body.access_token)
      router.push({name: 'index'})
    }
    else {
      alert.show(resp.body.msg)
      done()
    }
  }
</script>


<template>
  <AlertBox/>
  <h4 class="fw-bolder mb-3">login</h4>
  <BasicForm
    :inputs="inputs"
    @update="setInputValue"
    @submit="login"
  />
</template>

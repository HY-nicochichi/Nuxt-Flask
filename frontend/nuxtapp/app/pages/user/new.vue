<script setup lang="ts">
  import AlertBox from '~/components/AlertBox.vue'
  import FormArea from '~/components/FormArea.vue'
  import InputField from '~/components/InputField.vue'
  import SubmitButton from '~/components/SubmitButton.vue'
  import {bffAuthRoute, bffUserRoute} from '#shared'
  import {accessBff} from '~/composables/BffClient'
  import {validateEmail, validateName, validatePassword} from '~/composables/Validation'
  import {useAlertStore} from '~/stores'
  import type {Input} from '~/types'

  useHead({title: 'new user'})

  const router = useRouter()
  const alert = useAlertStore()

  const inputs: Ref<[Input, Input, Input]> = ref([
    {label: 'email', type: 'text', value: '', validation: validateEmail},
    {label: 'password', type: 'password', value: '', validation: validatePassword},
    {label: 'name', type: 'text', value: '', validation: validateName}
  ])

  const submitting: Ref<boolean> = ref(false)

  async function createUser(): Promise<void> {
    submitting.value = true
    const res1 = await accessBff(
      bffUserRoute, 'POST', {
        email: inputs.value[0].value,
        password: inputs.value[1].value,
        name: inputs.value[2].value
      }
    )
    if (res1.status === 201) {
      const res2 = await accessBff(
        bffAuthRoute + '/login', 'POST', {
          email: inputs.value[0].value, password: inputs.value[1].value
        }
      )
      router.push({name: res2.status === 200 ? 'index' : 'login'})
    }
    else {
      alert.show(res1.data?.msg)
      submitting.value = false
    }
  }
</script>


<template>
  <AlertBox/>
  <h1 class="fs-4 fw-bolder mb-3">new user</h1>
  <FormArea>
    <InputField
      v-for="(input, index) in inputs" :key="index"
      :label="input.label" :type="input.type" v-model="input.value"
    />
    <br>
    <SubmitButton
      :invalid="inputs.some((input) => !input.validation(input.value))"
      :submitting="submitting" :click="createUser"
    />
  </FormArea>
</template>

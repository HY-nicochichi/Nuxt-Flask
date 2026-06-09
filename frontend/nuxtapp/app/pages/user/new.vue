<script setup lang="ts">
  import AlertBox from '~/components/AlertBox.vue'
  import FormArea from '~/components/FormArea.vue'
  import InputField from '~/components/InputField.vue'
  import SubmitButton from '~/components/SubmitButton.vue'
  import {
    accessBff, bff_auth_route, bff_user_route
  } from '~/composables/ApiClient'
  import {
    validateEmail, validateName, validatePassword
  } from '~/composables/Validation'
  import {useAlertStore} from '~/stores'
  import type {Input, Resp} from '~/types'

  useHead({title: 'new user'})

  const router = useRouter()
  const alert = useAlertStore()

  const inputs: Ref<[Input, Input, Input]> = ref([
    {
      label: 'email',
      type: 'text',
      value: '',
      validation: validateEmail
    },
    {
      label: 'password',
      type: 'password',
      value: '',
      validation: validatePassword
    },
    {
      label: 'name',
      type: 'text',
      value: '',
      validation: validateName
    }
  ])

  const submitting: Ref<boolean> = ref(false)

  async function createUser(): Promise<void> {
    submitting.value = true
    const resp1: Resp = await accessBff(
      bff_user_route, 'POST',
      {
        email: inputs.value[0].value,
        password: inputs.value[1].value,
        name: inputs.value[2].value
      }
    )
    if (resp1.status === 204) {
      const resp2: Resp = await accessBff(
        bff_auth_route + 'login', 'POST',
        {
          email: inputs.value[0].value,
          password: inputs.value[1].value
        }
      )
      router.push({name: resp2.status === 200 ? 'index' : 'login'})
    }
    else {
      alert.show(resp1.body.msg)
      submitting.value = false
    }
  }
</script>


<template>
  <AlertBox/>
  <h4 class="fw-bolder mb-3">new user</h4>
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

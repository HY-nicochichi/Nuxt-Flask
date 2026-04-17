<script setup lang="ts">
  import AlertBox from '~/components/AlertBox.vue'
  import FormArea from '~/components/FormArea.vue'
  import InputField from '~/components/InputField.vue'
  import SubmitButton from '~/components/SubmitButton.vue'
  import {accessUserPatch} from '~/composables/ApiClient'
  import {validateEmail, validatePassword, validateName} from '~/composables/Validation'
  import {useAlertStore, useUserStore} from '~/stores'
  import type {Input, Resp} from '~/types'

  const router = useRouter()
  const route = useRoute()

  const param = route.params.param as string

  if (!['email', 'password', 'name'].includes(param)) {
    router.push('/404')
  }

  useHead({title: 'update user'})

  const alert = useAlertStore()
  const user = useUserStore()

  const currentPasswordInput: Input = {
    label: 'current password',
    type: 'password',
    value: '',
    validation: validatePassword
  }
  const emailInput: Input = {
    label: 'email',
    type: 'text',
    value: user.value.email,
    validation: validateEmail
  }
  const passwordInput: Input = {
    label: 'password',
    type: 'password',
    value: '',
    validation: validatePassword
  }
  const nameInput: Input = {
    label: 'name',
    type: 'text',
    value: user.value.name,
    validation: validateName
  }

  const inputs = ref([
    currentPasswordInput, {
      email: emailInput, password: passwordInput, name: nameInput
    }[param]
  ]) as Ref<[Input, Input]>

  const submitting: Ref<boolean> = ref(false)

  async function updateUser(): Promise<void> {
    submitting.value = true
    const resp: Resp = await accessUserPatch({
      current_password: inputs.value[0].value,
      [param]: inputs.value[1].value
    })
    if (resp.status === 204) {
      router.push({name: 'index'})
    }
    else {
      alert.show(resp.body.msg)
      submitting.value = false
    }
  }
</script>


<template>
  <AlertBox/>
  <h4 class="fw-bolder mb-3">update user</h4>
  <FormArea>
    <InputField
      v-for="(input, index) in inputs" :key="index"
      :label="input.label" :type="input.type" v-model="input.value"
    />
    <br>
    <SubmitButton
      :invalid="inputs.some((input) => !input.validation(input.value))"
      :submitting="submitting" :click="updateUser"
    />
  </FormArea>
</template>

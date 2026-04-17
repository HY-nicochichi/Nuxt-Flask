<script setup lang="ts">
  import AlertBox from '~/components/AlertBox.vue'
  import FormArea from '~/components/FormArea.vue'
  import InputField from '~/components/InputField.vue'
  import SubmitButton from '~/components/SubmitButton.vue'
  import {accessJwtPost} from '~/composables/ApiClient'
  import {setJwt} from '~/composables/JwtManager'
  import {validateEmail, validatePassword} from '~/composables/Validation'
  import {useAlertStore} from '~/stores'
  import type {Input, Resp} from '~/types'

  useHead({title: 'login'})

  const router = useRouter()
  const alert = useAlertStore()

  const inputs: Ref<[Input, Input]> = ref([
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
    }
  ])

  const submitting: Ref<boolean> = ref(false)

  async function login(): Promise<void> {
    submitting.value = true
    const resp: Resp = await accessJwtPost(
      inputs.value[0].value, inputs.value[1].value
    )
    if (resp.status === 200) {
      setJwt(resp.body.access_token)
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
  <h4 class="fw-bolder mb-3">login</h4>
  <FormArea>
    <InputField
      v-for="(input, index) in inputs" :key="index"
      :label="input.label" :type="input.type" v-model="input.value"
    />
    <br>
    <SubmitButton
      :invalid="inputs.some((input) => !input.validation(input.value))"
      :submitting="submitting" :click="login"
    />
  </FormArea>
</template>

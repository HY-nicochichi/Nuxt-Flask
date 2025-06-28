<script setup lang="ts">
  const router = useRouter()
  const alert = useAlertStore()

  const email: Input = {
    label: ref('email'),
    type: ref('text'),
    model: ref('')
  }
  const password: Input = {
    label: ref('password'),
    type: ref('password'),
    model: ref('')
  }

  async function tryLogin(): Promise<void> {
    if (email.model.value === '' || password.model.value === '') {
      alert.value = {
        show: true,
        msg: 'Fill all input fields'
      }
      email.model.value = ''
      password.model.value = ''
    }
    else {
      const resp: Resp = await accessJwtPost(
        email.model.value, password.model.value
      )
      if (resp.status === 200) {
        setJwt(resp.json.access_token)
        router.push({name: 'index'})
      }
      else {
        alert.value = {
          show: true,
          msg: resp.json.msg
        }
        email.model.value = ''
        password.model.value = ''
      }
    }
  }

  const inputs: Input[] = [
    email, password
  ]
  const submit: Submit = {
    name: ref('login'), func: (e: MouseEvent) => {tryLogin()}
  }

  onBeforeMount(() => {
    document.title = 'login'
  })
</script>

<template>
  <div class="p-3">
    <AlertBox/>
    <h4 class="fw-bolder mb-3">
      login
    </h4>
    <Form v-bind:inputs="inputs" v-bind:submit="submit"/>
  </div>
</template>

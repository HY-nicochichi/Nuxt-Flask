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
  const name: Input = {
    label: ref('name'),
    type: ref('text'),
    model: ref('')
  }

  async function tryCreateUser(): Promise<void> {
    if ( email.model.value === '' || password.model.value === '' || name.model.value === '') {
      alert.value = {
        show: true,
        msg: 'Fill all input fields'
      }
      email.model.value = ''
      password.model.value = ''
      name.model.value = ''
    }
    else {
      const resp1: Resp = await accessUserPost(
        email.model.value, password.model.value, name.model.value
      )
      if (resp1.status === 200) {
        const resp2: Resp = await accessJwtPost(
          email.model.value, password.model.value
        )
        setJwt(resp2.json.access_token)
        router.push({name: 'index'})
      }
      else {
        alert.value = {
          show: true,
          msg: resp1.json.msg
        }
        email.model.value = ''
        password.model.value = ''
        name.model.value = ''
      }
    }
  }

  const inputs: Input[] = [
    email, password, name
  ]
  const submit: Submit = {
    name: ref('create'), func: (e: MouseEvent) => {tryCreateUser()}
  }

  onBeforeMount(() => {
    document.title = 'new user'
  })
</script>

<template>
  <div class="p-3">
    <AlertBox/>
    <h4 class="fw-bolder mb-3">
      new user
    </h4>
    <Form v-bind:inputs="inputs" v-bind:submit="submit"/>
  </div>
</template>

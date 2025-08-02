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

  const inputs: Input[] = [email, password, name]

  async function tryCreateUser(): Promise<void> {
    if (inputs.some(input => input.model.value === '')) {
      alert.value = {
        show: true,
        msg: 'Fill all input fields'
      }
      for (const input of inputs) {
        input.model.value = ''
      }
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
        for (const input of inputs) {
          input.model.value = ''
        }
      }
    }
  }

  const submit: Submit = {
    name: 'create', func: (e: MouseEvent) => {tryCreateUser()}
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

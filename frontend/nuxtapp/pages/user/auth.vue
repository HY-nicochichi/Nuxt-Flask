<script setup lang="ts">
const router = useRouter()

let user: Ref<User> = ref({
  login: false,
  name: '',
  email: ''
})

let alert: Ref<Alert> = ref({
  show: false,
  msg: ''
})

let email: Ref<string> = ref('')
let password: Ref<string> = ref('')

async function checkLoggedIn(): Promise<void> {
  const resp: Resp = await accessUserGet()
  if (resp.status === 200) {
    router.push({name: 'index'})
  }
  else {
    setJwt()
  }
}

async function tryLogin(): Promise<void> {
  if (email.value === '' || password.value === '') {
    alert.value = {
      show: true,
      msg: 'Fill all input fields'
    }
    email.value = ''
    password.value = ''
  }
  else {
    const resp: Resp = await accessJwtPost(
      email.value, password.value
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
      email.value = ''
      password.value = ''
    }
  }
}

onBeforeMount(() => {
  document.title = 'login'
  checkLoggedIn()
})
</script>

<template>
  <NavBar v-bind:user="user"/>
  <div class="p-3">
    <AlertBox v-bind:alert="alert"/>
    <h4 class="fw-bolder mb-3">
      login
    </h4>
    <div class="col-sm-9 col-md-7 col-lg-5 border border-primary bg-light p-3">
      <div class="mb-4">
        <label class="mb-2">email</label>
        <input type="text" class="form-control border border-primary" v-model="email"/>
      </div>
      <div class="mb-4">
        <label class="mb-2">password</label>
        <input type="password" class="form-control border border-primary" v-model="password"/>
      </div>
      <br>
      <div>
        <button class="btn btn-primary" v-on:click="tryLogin">login</button>
      </div>
    </div>
  </div>
</template>

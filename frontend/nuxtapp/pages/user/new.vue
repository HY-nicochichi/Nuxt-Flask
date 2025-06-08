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
let name: Ref<string> = ref('')

async function checkLoggedIn(): Promise<void> {
  const resp: Resp = await accessUserGet()
  if (resp.status === 200) {
    router.push({name: 'index'})
  }
  else {
    setJwt()
  }
}

async function tryCreateUser(): Promise<void> {
  if (email.value === '' || password.value === '' || name.value === '') {
    alert.value = {
      show: true,
      msg: 'Fill all input fields'
    }
    email.value = ''
    password.value = ''
    name.value = ''
  }
  else {
    const resp1: Resp = await accessUserPost(
      email.value, password.value, name.value
    )
    if (resp1.status === 200) {
      const resp2: Resp = await accessJwtPost(
        email.value, password.value
      )
      setJwt(resp2.json.access_token)
      router.push({name: 'index'})
    }
    else {
      alert.value = {
        show: true,
        msg: resp1.json.msg
      }
      email.value = ''
      password.value = ''
      name.value = ''
    }
  }
}

onBeforeMount(() => {
  document.title = 'new user'
  checkLoggedIn()
})
</script>

<template>
  <NavBar v-bind:user="user"/>
  <div class="p-3">
    <AlertBox v-bind:alert="alert"/>
    <h4 class="fw-bolder mb-3">
      new user
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
      <div class="mb-4">
        <label class="mb-2">name</label>
        <input type="text" class="form-control border border-primary" v-model="name"/>
      </div>
      <br>
      <div>
        <button class="btn btn-primary" v-on:click="tryCreateUser">create</button>
      </div>
    </div>
  </div>
</template>

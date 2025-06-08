<script setup lang="ts">
const router = useRouter()

let user: Ref<User> = ref({
  login: false,
  name: '',
  email: ''
})

async function setUserInfo(): Promise<void> {
  const resp: Resp = await accessUserGet()
  if (resp.status === 200) {
    user.value = {
      login: true,
      name: resp.json.name,
      email: resp.json.email
    }
  }
  else {
    setJwt()
    router.push({name: 'user-auth'})
  }
}

function confirmDeleteUser(): void {
  if (confirm('Comfirm user deletion?') === true) {
    accessUserDelete()
    setJwt()
    router.push({name: 'index'})
  }
}

onBeforeMount(() => {
  document.title = 'user info'
  setUserInfo()
})
</script>

<template>
  <NavBar v-bind:user="user"/>
  <div class="p-3">
    <h4 class="fw-bolder mb-3">
      user info
    </h4>
    <div class="col-sm-9 col-md-6 col-lg-4 border border-primary bg-light mt-4 p-3">
      name：{{ user.name }}
      <br>
      <NuxtLink to="/user/update/name" class="btn btn-primary my-2">
        update
      </NuxtLink>
      <br>
      <hr class="border-primary">
      email：{{ user.email }}
      <br>
      <NuxtLink to="/user/update/email" class="btn btn-primary my-2">
        update
      </NuxtLink>
      <br>
      <hr class="border-primary">
      password：＊＊＊＊＊＊
      <br>
      <NuxtLink to="/user/update/password" class="btn btn-primary my-2">
        update
      </NuxtLink>
    </div>
    <br>
    <div class="my-2">
      <NuxtLink class="btn btn-danger" v-on:click.prevent="confirmDeleteUser">
        delete account
      </NuxtLink>
    </div>
    <br>
  </div>
</template>

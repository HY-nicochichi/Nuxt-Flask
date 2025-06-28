<script setup lang="ts">
  const router = useRouter()
  const user = useUserStore()

  async function confirmDeleteUser(): Promise<void> {
    if (confirm('Comfirm user deletion?')) {
      await accessUserDelete()
      setJwt()
      router.push({name: 'index'})
    }
  }

  onBeforeMount(() => {
    document.title = 'user info'
  })
</script>

<template>
  <div class="p-3">
    <h4 class="fw-bolder mb-3">
      user info
    </h4>
    <div class="col-sm-9 col-md-6 col-lg-4 border border-primary bg-light mt-4 p-3">
      name：{{ user.value.name }}
      <br>
      <NuxtLink to="/user/update/name" class="btn btn-primary my-2">
        update
      </NuxtLink>
      <br>
      <hr class="border-primary">
      email：{{ user.value.email }}
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

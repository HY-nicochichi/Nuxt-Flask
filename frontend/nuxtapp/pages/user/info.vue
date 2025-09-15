<script setup lang="ts">
  useHead({title: 'user info'})

  async function confirmDeleteUser(): Promise<void> {
    if (confirm('Comfirm user deletion?')) {
      const resp = await accessUserDelete()
      if (resp.status === 204) {
        setJwt()
        useRouter().push({name: 'index'})
      }
    }
  }
</script>

<template>
  <h4 class="fw-bolder mb-3">user info</h4>
  <div class="col-sm-9 col-md-6 col-lg-4 border border-primary bg-light mt-4 p-3">
    name：{{ useUserStore().value.name }}
    <br>
    <NuxtLink to="/user/update/name" class="btn btn-primary my-2">
      update
    </NuxtLink>
    <br>
    <hr class="border-primary">
    email：{{ useUserStore().value.email }}
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
</template>

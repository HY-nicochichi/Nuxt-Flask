<script setup lang="ts">
  import {LoadingSpinner} from '~/components/SvgIcons'
  import {accessProtectedBff, bffUserRoute, bffAuthRoute} from '~/composables/ApiClient'
  import {useUserStore} from '~/stores'
  import type {Resp} from '~/types'

  useHead({title: 'user info'})

  const router = useRouter()
  const user = useUserStore()

  const deleting: Ref<boolean> = ref(false)

  async function deleteUser(): Promise<void> {
    if (confirm('Comfirm user deletion?')) {
      deleting.value = true
      const resp: Resp = await accessProtectedBff(bffUserRoute + '/me', 'DELETE')
      if (resp.status === 204) {
        await accessProtectedBff(bffAuthRoute + '/logout', 'GET')
        router.push({name: 'index'})
      }
      deleting.value = false
    }
  }
</script>


<template>
  <h1 class="fs-4 fw-bolder mb-3">user info</h1>
  <section role="group" class="col-sm-9 col-md-7 col-lg-5 bg-primary bg-opacity-25 p-3">
    <div class="mb-2">name：{{ user.value.name }}</div>
    <NuxtLink to="/user/update/name" class="btn btn-primary">
      update
    </NuxtLink>
    <hr>
    <div class="mb-2">email：{{ user.value.email }}</div>
    <NuxtLink to="/user/update/email" class="btn btn-primary">
      update
    </NuxtLink>
    <hr>
    <div class="mb-2">password：＊＊＊＊＊＊＊＊</div>
    <NuxtLink to="/user/update/password" class="btn btn-primary">
      update
    </NuxtLink>
  </section>
  <br>
  <NuxtLink class="btn btn-danger" @click.prevent="deleteUser">
    <LoadingSpinner v-if="deleting" class="mx-4" :size="'25'" :color="'white'"/>
    <span v-else>delete user</span>
  </NuxtLink>
</template>


<style scoped>
  section {
    border-style: solid;
    border-width: 2px;
    border-radius: 0.5rem;
    border-color: var(--color-text);
  }

  hr {
    border-style: solid;
    border-width: 1px;
    border-color: var(--color-text);
  }
</style>

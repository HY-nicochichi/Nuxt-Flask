<script setup lang="ts">
  import {LoadingSpinner} from '~/components/SvgIcons'
  import FormArea from '~/components/FormArea.vue'
  import {accessBff, bff_user_route} from '~/composables/ApiClient'
  import {useUserStore} from '~/stores'
  import type {Resp} from '~/types'

  useHead({title: 'user info'})

  const router = useRouter()
  const user = useUserStore()

  const deleting: Ref<boolean> = ref(false)

  async function deleteUser(): Promise<void> {
    if (confirm('Comfirm user deletion?')) {
      deleting.value = true
      const resp: Resp = await accessBff(bff_user_route, 'DELETE')
      if (resp.status === 204) router.push({name: 'index'})
      deleting.value = false
    }
  }
</script>


<template>
  <h4 class="fw-bolder mb-3">user info</h4>
  <FormArea>
    <div class="mb-2">name：{{ user.value.name }}</div>
    <NuxtLink to="/user/update/name" class="btn btn-primary">
      update
    </NuxtLink>
    <hr class="border-white">
    <div class="mb-2">email：{{ user.value.email }}</div>
    <NuxtLink to="/user/update/email" class="btn btn-primary">
      update
    </NuxtLink>
    <hr class="border-white">
    <div class="mb-2">password：＊＊＊＊＊＊＊＊</div>
    <NuxtLink to="/user/update/password" class="btn btn-primary">
      update
    </NuxtLink>
  </FormArea>
  <br>
  <NuxtLink class="btn btn-danger" @click.prevent="deleteUser">
    <LoadingSpinner v-if="deleting" class="mx-4" :size="'25'" :color="'white'"/>
    <span v-else>delete user</span>
  </NuxtLink>
</template>

<script setup lang="ts">
  import {LoadingSpinner} from '~/components/SvgIcons'
  import {accessUserDelete} from '~/composables/ApiClient'
  import {setJwt} from '~/composables/JwtManager'
  import {useUserStore} from '~/stores'

  useHead({title: 'user info'})

  const router = useRouter()
  const user = useUserStore()

  const deleting: Ref<boolean> = ref(false)

  async function deleteUser(): Promise<void> {
    if (confirm('Comfirm user deletion?')) {
      deleting.value = true
      const resp = await accessUserDelete()
      if (resp.status === 204) {
        setJwt()
        router.push({name: 'index'})
      }
      else {
        deleting.value = false
      }
    }
  }
</script>


<template>
  <h4 class="fw-bolder mb-3">user info</h4>
  <div class="col-sm-9 col-md-6 col-lg-4 bg-white bg-opacity-25 border border-white rounded mt-4 p-3">
    name：{{ user.value.name }}
    <br>
    <NuxtLink to="/user/update/name" class="btn btn-primary my-2">
      update
    </NuxtLink>
    <br>
    <hr class="border-white">
    email：{{ user.value.email }}
    <br>
    <NuxtLink to="/user/update/email" class="btn btn-primary my-2">
      update
    </NuxtLink>
    <br>
    <hr class="border-white">
    password：＊＊＊＊＊＊
    <br>
    <NuxtLink to="/user/update/password" class="btn btn-primary my-2">
      update
    </NuxtLink>
  </div>
  <br>
  <div class="my-2">
    <NuxtLink class="btn btn-danger" @click.prevent="deleteUser">
      <LoadingSpinner
        v-if="deleting" class="mx-4"
        :size="'25'" :color="'white'"
      />
      <span v-else>delete user</span>
    </NuxtLink>
  </div>
</template>

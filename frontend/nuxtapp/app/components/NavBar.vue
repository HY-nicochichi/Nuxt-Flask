<script setup lang="ts">
  import {BrandLogo, HamburgerMenu} from '~/components/SvgIcons'
  import {setJwt} from '~/composables/JwtManager'
  import {useUserStore} from '~/stores'

  const route = useRoute()
  const router = useRouter()
  const user = useUserStore()

  function logout(): void {
    setJwt()
    if (route.name === 'index') {
      router.go(0)
    } else {
      router.push({name: 'index'})
    }
  }
</script>


<template>
  <div class="pt-3">
    <nav class="navbar navbar-expand-sm navbar-dark bg-primary px-3 py-2">
      <NuxtLink to="/" class="navbar-brand color-dark d-flex align-items-center">
        <BrandLogo :size="'35'" :color="'mediumspringgreen'"/>
        <span class="ps-2 fs-4 fw-bolder">Nuxt-Flask</span>
      </NuxtLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#NavBarContent" aria-controls="NavBarContent" aria-expanded="false" aria-label="Toggle navigation">
        <HamburgerMenu :size="'35'" :color="'white'"/>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="NavBarContent">
        <ul v-if="user.value.login" class="navbar-nav">
          <li class="nav-item">
            <NuxtLink to="/user/info" class="nav-link active fw-bolder me-2">
              {{ user.value.name }}
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink class="nav-link active fw-bolder" @click="logout">
              logout
            </NuxtLink>
          </li>
        </ul>
        <ul v-else class="navbar-nav">
          <li class="nav-item">
            <NuxtLink to="/login" class="nav-link active fw-bolder me-2">
              login
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/user/new" class="nav-link active fw-bolder">
              new user
            </NuxtLink>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>

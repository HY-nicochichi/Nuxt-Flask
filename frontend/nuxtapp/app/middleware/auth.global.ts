import {accessUserGet} from '~/composables/ApiClient'
import {setJwt} from '~/composables/JwtManager'
import {useAlertStore, useUserStore} from '~/stores'
import type {Resp} from '~/types'

export default defineNuxtRouteMiddleware(async(to, _) => {
  const alert = useAlertStore()
  const user = useUserStore()

  alert.clear()

  const resp: Resp = await accessUserGet()

  if (resp.status === 200) {
    user.login(resp.body.email, resp.body.name)
  }
  else {
    user.clear()
    setJwt()
  }

  const NoAuthRoutes: string[] = ['login', 'user-new']
  const targetRoute = to.name as string

  if (targetRoute !== 'index'){
    if (user.value.login && NoAuthRoutes.includes(targetRoute)) {
      return navigateTo({name: 'index'})
    }
    if (!user.value.login && !NoAuthRoutes.includes(targetRoute)) {
      return navigateTo({name: 'login'})
    }
  }
})

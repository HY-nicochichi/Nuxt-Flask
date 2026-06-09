import {
  accessBff, bff_user_route
} from '~/composables/ApiClient'
import {useAlertStore, useUserStore} from '~/stores'
import type {Resp} from '~/types'

export default defineNuxtRouteMiddleware(async(to, _) => {
  useAlertStore().clear()
  const user = useUserStore()

  const resp: Resp = await accessBff(bff_user_route, 'GET')
  resp.status === 200 ? user.login(resp.body.email, resp.body.name) : user.clear()

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

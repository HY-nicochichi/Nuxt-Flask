import {bffUserRoute} from '#shared'
import {accessProtectedBff} from '~/composables/BffClient'
import {useAlertStore, useUserStore} from '~/stores'

export default defineNuxtRouteMiddleware(async(to, _) => {
  useAlertStore().clear()
  const user = useUserStore()

  const res = await accessProtectedBff(bffUserRoute + '/me', 'GET')
  res.status === 200 ? user.login(res.data?.email, res.data?.name) : user.clear()

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

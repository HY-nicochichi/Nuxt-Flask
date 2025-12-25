import {accessUserGet} from '../composables/ApiClient'
import {setJwt} from '../composables/JwtManager'
import {useUserStore} from '../stores/UserStore'

export default defineNuxtRouteMiddleware(async(to, from) => {
  const user = useUserStore()
  const resp: Resp = await accessUserGet()

  if (resp.status === 200) {
    user.loginUser(resp.body.email, resp.body.name)
  }
  else {
    user.clear()
    setJwt()
  }

  const NoAuthRoutes: string[] = ['login', 'user-new']

  if (to.name !== 'index'){
    if (user.value.login && NoAuthRoutes.includes(to.name as string)) {
      return navigateTo({name: 'index'})
    }
    if (!user.value.login && !NoAuthRoutes.includes(to.name as string)) {
      return navigateTo({name: 'login'})
    }
  }
})

export default defineNuxtRouteMiddleware(async(to, from) => {
  const user = useUserStore()
  const resp: Resp = await accessUserGet()

  if (resp.status === 200) {
    user.loginUser(resp.json.email, resp.json.name)
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

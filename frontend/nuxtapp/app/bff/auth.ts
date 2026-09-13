import {Hono} from 'hono'
import {getTokenCookie, setTokenCookie, deleteTokenCookie} from '~/bff/cookie'
import {accessApi, apiTokenRoute} from '~/composables/ApiClient'
import type {Resp} from '~/types'

const authRouter = new Hono()

authRouter.post('/login', async(c) => {
  const resp: Resp = await accessApi(
    apiTokenRoute, 'POST', await c.req.json()
  )
  if (resp.status === 200) {
    await setTokenCookie(c, 'access', resp.body.access_token)
    await setTokenCookie(c, 'refresh', resp.body.refresh_token)
    return c.json({msg: 'Logged in successfully'}, 200)
  }
  else {
    return c.json(resp.body, resp.status)
  }
})

authRouter.post('/refresh', async(c) => {
  const resp: Resp = await accessApi(
    apiTokenRoute + '/refresh', 'POST', undefined, await getTokenCookie(c, 'refresh')
  )
  if (resp.status === 200) {
    await setTokenCookie(c, 'access', resp.body.access_token)
    return c.json({msg: 'Refreshed successfully'}, 200)
  }
  else {
    return c.json(resp.body, resp.status)
  }
})

authRouter.get('/logout', async(c) => {
  deleteTokenCookie(c, 'access')
  deleteTokenCookie(c, 'refresh')
  return c.json({msg: 'Logged out successfully'}, 200)
})

export default authRouter

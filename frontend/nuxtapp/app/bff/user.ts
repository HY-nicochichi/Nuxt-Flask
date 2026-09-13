import {Hono} from 'hono'
import {getTokenCookie} from '~/bff/cookie'
import {accessApi, apiUserRoute} from '~/composables/ApiClient'
import type {Resp} from '~/types'

const userRouter = new Hono()

userRouter.post('', async(c) => {
  const resp: Resp = await accessApi(
    apiUserRoute, 'POST', await c.req.json()
  )
  return resp.status === 204 ? c.body(null, 204) : c.json(resp.body, resp.status)
})

userRouter.get('/me', async(c) => {
  const resp: Resp = await accessApi(
    apiUserRoute + '/me', 'GET', undefined, await getTokenCookie(c, 'access')
  )
  return c.json(resp.body, resp.status)
})

userRouter.patch('/me', async(c) => {
  const resp: Resp = await accessApi(
    apiUserRoute + '/me', 'PATCH', await c.req.json(), await getTokenCookie(c, 'access')
  )
  return resp.status === 204 ? c.body(null, 204) : c.json(resp.body, resp.status)
})

userRouter.delete('/me', async(c) => {
  const resp: Resp = await accessApi(
    apiUserRoute + '/me', 'DELETE', undefined, await getTokenCookie(c, 'access')
  ) 
  return resp.status === 204 ? c.body(null, 204) : c.json(resp.body, resp.status)
})

export default userRouter

import {Hono} from 'hono'
import type {ContentfulStatusCode} from 'hono/utils/http-status'
import {getTokenCookie} from '~/bff/cookie'
import {accessApi, apiUserRoute, bffUserRoute} from '~/composables/ApiClient'
import type {Resp} from '~/types'

const userRouter = new Hono()

userRouter.post('', async(c) => {
  const resp: Resp = await accessApi(
    apiUserRoute, 'POST', await c.req.json()
  )
  return resp.status === 201 ?
    c.body(null, 201, {Location: bffUserRoute + '/me'}) :
    c.json(resp.data, resp.status as ContentfulStatusCode)
})

userRouter.get('/me', async(c) => {
  const resp: Resp = await accessApi(
    apiUserRoute + '/me', 'GET', undefined, await getTokenCookie(c, 'access')
  )
  return c.json(resp.data, resp.status as ContentfulStatusCode)
})

userRouter.patch('/me', async(c) => {
  const resp: Resp = await accessApi(
    apiUserRoute + '/me', 'PATCH', await c.req.json(), await getTokenCookie(c, 'access')
  )
  return resp.status === 204 ?
    c.body(null, 204) : c.json(resp.data, resp.status as ContentfulStatusCode)
})

userRouter.delete('/me', async(c) => {
  const resp: Resp = await accessApi(
    apiUserRoute + '/me', 'DELETE', undefined, await getTokenCookie(c, 'access')
  ) 
  return resp.status === 204 ?
    c.body(null, 204) : c.json(resp.data, resp.status as ContentfulStatusCode)
})

export default userRouter

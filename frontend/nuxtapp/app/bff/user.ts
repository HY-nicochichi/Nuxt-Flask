import {Hono} from 'hono'
import {getCookie} from 'hono/cookie'
import {decryptToken} from './encrypt'
import {accessApi, api_user_route} from '~/composables/ApiClient'
import type {Resp} from '~/types'

const user_router = new Hono()

user_router.post('', async(c) => {
  const resp: Resp = await accessApi(
    api_user_route, 'POST', await c.req.json()
  )
  return resp.status === 204 ? c.body(null, 204) : c.json(resp.body, resp.status)
})

user_router.get('/me', async(c) => {
  const resp: Resp = await accessApi(
    api_user_route + '/me', 'GET', undefined,
    decryptToken(getCookie(c, 'access_token_enc'))
  )
  return c.json(resp.body, resp.status)
})

user_router.patch('/me', async(c) => {
  const resp: Resp = await accessApi(
    api_user_route + '/me', 'PATCH', await c.req.json(),
    decryptToken(getCookie(c, 'access_token_enc'))
  )
  return resp.status === 204 ? c.body(null, 204) : c.json(resp.body, resp.status)
})

user_router.delete('/me', async(c) => {
  const resp: Resp = await accessApi(
    api_user_route + '/me', 'DELETE', undefined,
    decryptToken(getCookie(c, 'access_token_enc'))
  ) 
  return resp.status === 204 ? c.body(null, 204) : c.json(resp.body, resp.status)
})

export default user_router

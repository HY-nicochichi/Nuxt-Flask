import {Hono} from 'hono'
import {getCookie, deleteCookie} from 'hono/cookie'
import {accessApi, api_user_route} from '~/composables/ApiClient'
import type {Resp} from '~/types'

const user_router = new Hono()

user_router.post('/', async(c) => {
  const resp: Resp = await accessApi(
    api_user_route, 'POST', await c.req.json()
  )
  return resp.status === 204 ? c.body(null, 204) : c.json(resp.body, resp.status)
})

user_router.get('/', async(c) => {
  const resp: Resp = await accessApi(
    api_user_route, 'GET', undefined, getCookie(c, 'access_token')
  )
  return c.json(resp.body, resp.status)
})

user_router.patch('/', async(c) => {
  const resp: Resp = await accessApi(
    api_user_route, 'PATCH', await c.req.json(), getCookie(c, 'access_token')
  )
  return resp.status === 204 ? c.body(null, 204) : c.json(resp.body, resp.status)
})

user_router.delete('/', async(c) => {
  const resp: Resp = await accessApi(
    api_user_route, 'DELETE', undefined, getCookie(c, 'access_token')
  ) 
  if(resp.status === 204) {
    deleteCookie(c, 'access_token')
    return c.body(null, 204)
  }
  else {
    return c.json(resp.body, resp.status)
  }
})

export default user_router

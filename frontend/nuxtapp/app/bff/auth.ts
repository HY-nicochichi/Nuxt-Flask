import {Hono} from 'hono'
import {setCookie, deleteCookie} from 'hono/cookie'
import {accessApi, api_jwt_route} from '~/composables/ApiClient'
import type {Resp} from '~/types'

const auth_router = new Hono()

auth_router.post('/login', async(c) => {
  const resp: Resp = await accessApi(
    api_jwt_route, 'POST', await c.req.json()
  )
  if (resp.status === 200) {
    setCookie(c, 'access_token', resp.body.access_token, {
      httpOnly: true,
      secure: process.env.FORCE_SSL_COOKIE === '1',
      sameSite: 'Strict'
    })
    return c.json({msg: 'Logged in successfully'}, 200)
  }
  else {
    return c.json(resp.body, resp.status)
  }
})

auth_router.get('/logout', (c) => {
  deleteCookie(c, 'access_token')
  return c.json({msg: 'Logged out successfully'}, 200)
})

export default auth_router

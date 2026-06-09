import {Hono} from 'hono'
import {getCookie, setCookie, deleteCookie} from 'hono/cookie'
import {encryptToken, decryptToken} from './encrypt'
import {accessApi, api_token_route} from '~/composables/ApiClient'
import type {Resp} from '~/types'

const auth_router = new Hono()

auth_router.post('/login', async(c) => {
  const resp: Resp = await accessApi(
    api_token_route, 'POST', await c.req.json()
  )
  if (resp.status === 200) {
    setCookie(c, 'access_token_enc', encryptToken(resp.body.access_token), {
      httpOnly: true,
      secure: process.env.FORCE_SSL_COOKIE === '1',
      sameSite: 'Strict',
      path: '/bff'
    })
    setCookie(c, 'refresh_token_enc', encryptToken(resp.body.refresh_token), {
      httpOnly: true,
      secure: process.env.FORCE_SSL_COOKIE === '1',
      sameSite: 'Strict',
      path: '/bff/auth'
    })
    return c.json({msg: 'Logged in successfully'}, 200)
  }
  else {
    return c.json(resp.body, resp.status)
  }
})

auth_router.post('/refresh', async(c) => {
  const resp: Resp = await accessApi(
    api_token_route + '/refresh', 'POST', undefined,
    decryptToken(getCookie(c, 'refresh_token_enc'))
  )
  if (resp.status === 200) {
    setCookie(c, 'access_token_enc', resp.body.access_token, {
      httpOnly: true,
      secure: process.env.FORCE_SSL_COOKIE === '1',
      sameSite: 'Strict',
      path: '/bff'
    })
    return c.json({msg: 'Refreshed successfully'}, 200)
  }
  else {
    return c.json(resp.body, resp.status)
  }
})

auth_router.get('/logout', async(c) => {
  deleteCookie(c, 'access_token_enc', {path: '/bff'})
  deleteCookie(c, 'refresh_token_enc', {path: '/bff/auth'})
  return c.json({msg: 'Logged out successfully'}, 200)
})

export default auth_router

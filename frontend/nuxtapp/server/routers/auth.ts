import {Hono} from 'hono'
import {proxyToApi} from '#server/proxy'
import {setTokenCookie, deleteTokenCookie} from '#server/cookie'

const apiTokenRoute = '/tokens'
export const authRouter = new Hono()

authRouter.post('/login', async(c) => {
  const res = await proxyToApi(c, apiTokenRoute)
  if (res.status !== 200) return res
  const data = await res.json()
  await setTokenCookie(c, 'access', data.access_token)
  await setTokenCookie(c, 'refresh', data.refresh_token)
  return c.json({msg: 'Logged in successfully'}, 200)
})

authRouter.post('/refresh', async(c) => {
  const res = await proxyToApi(c, apiTokenRoute + '/refresh', 'refresh')
  if (res.status !== 200) return res
  const data = await res.json()
  await setTokenCookie(c, 'access', data.access_token)
  return c.json({msg: 'Refreshed successfully'}, 200)
})

authRouter.post('/logout', async(c) => {
  deleteTokenCookie(c, 'access')
  deleteTokenCookie(c, 'refresh')
  return c.json({msg: 'Logged out successfully'}, 200)
})

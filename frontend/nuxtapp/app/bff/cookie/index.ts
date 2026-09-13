import {Context} from 'hono'
import {getSignedCookie, setSignedCookie, deleteCookie} from 'hono/cookie'
import {bffAuthRoute} from '~/composables/ApiClient'

const bffCookieSecret: string = process.env.BFF_COOKIE_SECRET as string
const forceSslCookie: boolean = process.env.FORCE_SSL_COOKIE === '1'

async function getTokenCookie(
  c: Context, type: 'access'|'refresh'
): Promise<string|undefined> {
  return await getSignedCookie(c, bffCookieSecret, type + '_token') || undefined
}

async function setTokenCookie(
  c: Context, type: 'access'|'refresh', token: string
): Promise<void> {
  await setSignedCookie(c, type + '_token', token, bffCookieSecret, {
    httpOnly: true,
    secure: forceSslCookie,
    sameSite: 'Strict',
    path: '/bff' + (type === 'refresh' ? bffAuthRoute : '')
  })
}

function deleteTokenCookie(c: Context, type: 'access'|'refresh'): void {
  deleteCookie(c, type + '_token', {
    path: '/bff' + (type === 'refresh' ? bffAuthRoute : '')
  })
}

export {getTokenCookie, setTokenCookie, deleteTokenCookie}

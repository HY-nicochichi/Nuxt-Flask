import {Context} from 'hono'
import {getSignedCookie, setSignedCookie, deleteCookie} from 'hono/cookie'
import {bffUrlBase, bffAuthRoute} from '#shared'

const bffCookieSecret = process.env.BFF_COOKIE_SECRET as string
const forceSslCookie: boolean = process.env.FORCE_SSL_COOKIE !== '0'

export type TokenType = 'access'|'refresh'

export async function getTokenCookie(
  c: Context, type: TokenType
): Promise<string|undefined> {
  return await getSignedCookie(c, bffCookieSecret, type + '_token') || undefined
}

export async function setTokenCookie(
  c: Context, type: TokenType, token: string
): Promise<void> {
  await setSignedCookie(c, type + '_token', token, bffCookieSecret, {
    httpOnly: true,
    secure: forceSslCookie,
    sameSite: 'Strict',
    path: bffUrlBase + (type === 'refresh' ? bffAuthRoute : ''),
    maxAge: 14*24*60*60
  })
}

export function deleteTokenCookie(c: Context, type: TokenType): void {
  deleteCookie(c, type + '_token', {
    path: bffUrlBase + (type === 'refresh' ? bffAuthRoute : '')
  })
}

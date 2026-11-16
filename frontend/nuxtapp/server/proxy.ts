import type {Context} from 'hono'
import {getTokenCookie, type TokenType} from '#server/cookie'
import {bffUrlBase} from '#shared'

const apiUrlBase = process.env.API_URL_BASE as string

async function reqToApi(
  c: Context, route: string, tokenType?: TokenType
): Promise<Request> {
  const headers = new Headers()
  const contentType = c.req.header('Content-Type')
  if (contentType) headers.set('Content-Type', contentType)
  if (tokenType) {
    const token = await getTokenCookie(c, tokenType)
    if (token) headers.set('Authorization', 'Bearer ' + token)
  }
  const body = c.req.raw.body ? await c.req.arrayBuffer() : undefined
  return new Request(
    apiUrlBase + route, {method: c.req.method, headers: headers, body: body}
  )
}

async function resToClient(res: Response): Promise<Response> {
  const headers = new Headers()
  const contentType = res.headers.get('Content-Type')
  const location = res.headers.get('Location')
  if (contentType) headers.set('Content-Type', contentType)
  if (location) headers.set('Location', bffUrlBase + location)
  const body = res.body ? await res.arrayBuffer() : undefined
  return new Response(body, {status: res.status, headers: headers})
}

export async function proxyToApi(
  c: Context, route: string, tokenType?: TokenType
): Promise<Response> {
  try {
    return await resToClient(await fetch(await reqToApi(c, route, tokenType)))
  }
  catch {
    return Response.json({msg: 'Internal Server Error'}, {status: 500})
  }
}

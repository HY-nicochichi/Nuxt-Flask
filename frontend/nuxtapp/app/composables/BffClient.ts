import {bffUrlBase, bffAuthRoute} from '#shared'

type Method = 'GET'|'POST'|'PATCH'|'DELETE'
type Res = {status: number, data?: Record<string, any>}

function reqToBff(
  route: string, method: Method, data?: Record<string, any>
): Request {
  const headers = new Headers()
  let body: string|undefined = undefined
  if (data && ['POST', 'PATCH'].includes(method)) {
    headers.set('Content-Type', 'application/json')
    body = JSON.stringify(data)
  }
  return new Request(
    bffUrlBase + route, {
      method: method, credentials: 'same-origin', headers: headers, body: body
    }
  )
}

export async function accessBff(
  route: string, method: Method, data?: Record<string, any>
): Promise<Res> {
  await new Promise(r => setTimeout(r, 300))  // simulate network delay
  try {
    const response: Response = await fetch(reqToBff(route, method, data))
    return {
      status: response.status,
      data: [201, 204].includes(response.status) ? undefined : await response.json()
    }
  }
  catch {
    return {status: 500, data: {msg: 'Unexpected error in network or server'}}
  }
}

export async function accessProtectedBff(
  route: string, method: Method, data?: Record<string, any>
): Promise<Res> {
  let res = await accessBff(route, method, data)
  if (res.status === 401 && res.data?.msg === 'Token has expired') {
    const refreshRes = await accessBff(bffAuthRoute + '/refresh', 'POST')
    if (refreshRes.status === 200) res = await accessBff(route, method, data)
  }
  return res
}

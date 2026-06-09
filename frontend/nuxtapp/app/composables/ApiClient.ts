import type {Req, Resp} from '~/types'

const api_token_route: string = '/tokens'
const api_user_route: string = '/users'

const bff_auth_route: string = '/auth'
const bff_user_route: string = '/users'

async function accessBackend(req: Req): Promise<Resp> {
  await new Promise(r => setTimeout(r, 300))  // simulate network delay
  try {
    const response: Response = await fetch(req.route, req.init)
    return {
      status: response.status,
      body: response.status === 204 ? '' : await response.json()
    }
  }
  catch(_) {
    return {
      status: 500,
      body: {msg: 'Unexpected error in network or server'}
    }
  }
}

async function accessApi(
  route: string,
  method: 'GET'|'POST'|'PATCH'|'DELETE',
  body?: Record<string, any>,
  token?: string
): Promise<Resp> {
  const req: Req = {
    route: process.env.API_URL_BASE + route,
    init: {
      credentials: 'omit',
      method: method,
      headers: token ? {Authorization: 'Bearer ' + token} : {},
    }
  }
  if (['POST', 'PATCH'].includes(method) && body) {
    req.init.headers['Content-Type'] = 'application/json'
    req.init.body = JSON.stringify(body)
  }
  return await accessBackend(req)
}

async function accessBff(
  route: string,
  method: 'GET'|'POST'|'PATCH'|'DELETE',
  body?: Record<string, any>
): Promise<Resp> {
  const req: Req = {
    route: '/bff' + route,
    init: {
      credentials: 'same-origin',
      method: method,
      headers: {}
    }
  }
  if (['POST', 'PATCH'].includes(method) && body) {
    req.init.headers['Content-Type'] = 'application/json'
    req.init.body = JSON.stringify(body)
  }
  return await accessBackend(req)
}

async function accessProtectedBff(
  route: string,
  method: 'GET'|'POST'|'PATCH'|'DELETE',
  body?: Record<string, any>
): Promise<Resp> {
  let resp: Resp = await accessBff(route, method, body)
  if (resp.status === 401 && resp.body.msg === 'Token has expired') {
    const refreshResp: Resp = await accessBff(bff_auth_route + '/refresh', 'POST')
    if (refreshResp.status === 200) {
      resp = await accessBff(route, method, body)
    }
  }
  return resp
}

export {
  api_token_route, api_user_route,
  bff_auth_route, bff_user_route,
  accessBackend, accessApi, accessBff, accessProtectedBff
}

import type {Req, Resp} from '~/types'

const api_jwt_route: string = '/jwt/'
const api_user_route: string = '/user/'

const bff_auth_route: string = '/auth/'
const bff_user_route: string = '/user/'

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
  access_token?: string
): Promise<Resp> {
  const req: Req = {
    route: process.env.API_URL_BASE + route,
    init: {
      mode: 'cors',
      credentials: 'omit',
      method: method,
      headers: access_token ? {Authorization: 'Bearer ' + access_token} : {},
    }
  }
  if (['POST', 'PATCH'].includes(method)) {
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
      mode: 'same-origin',
      credentials: 'same-origin',
      method: method,
      headers: {}
    }
  }
  if (['POST', 'PATCH'].includes(method)) {
    req.init.headers['Content-Type'] = 'application/json'
    req.init.body = JSON.stringify(body)
  }
  return await accessBackend(req)
}

export {
  api_jwt_route, api_user_route,
  bff_auth_route, bff_user_route,
  accessBackend,accessApi, accessBff
}

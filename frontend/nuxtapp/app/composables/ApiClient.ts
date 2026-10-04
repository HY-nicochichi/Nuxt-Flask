import type {Req, Resp} from '~/types'

const apiUrlBase: string = process.env.API_URL_BASE as string
const bffUrlBase: string = '/bff'

const apiTokenRoute: string = '/tokens'
const apiUserRoute: string = '/users'

const bffAuthRoute: string = '/auth'
const bffUserRoute: string = '/users'

function createReq(
  route: string,
  method: 'GET'|'POST'|'PATCH'|'DELETE',
  data?: Record<string, any>,
  token?: string
): Req {
  const req: Req = {
    route: route,
    init: {
      method: method,
      credentials: route.startsWith(apiUrlBase) ? 'omit' : 'same-origin',
      headers: token ? {Authorization: 'Bearer ' + token} : {}
    }
  }
  if (['POST', 'PATCH'].includes(method) && data) {
    req.init.headers['Content-Type'] = 'application/json'
    req.init.body = JSON.stringify(data)
  }
  return req
}

async function accessBackend(req: Req): Promise<Resp> {
  await new Promise(r => setTimeout(r, 300))  // simulate network delay
  try {
    const response: Response = await fetch(req.route, req.init)
    return {
      status: response.status,
      data: [201, 204].includes(response.status) ?
        undefined : await response.json()
    }
  }
  catch(_) {
    return {
      status: 500, data: {msg: 'Unexpected error in network or server'}
    }
  }
}

async function accessApi(
  route: string,
  method: 'GET'|'POST'|'PATCH'|'DELETE',
  data?: Record<string, any>,
  token?: string
): Promise<Resp> {
  const req: Req = createReq(apiUrlBase + route, method, data, token)
  return await accessBackend(req)
}

async function accessBff(
  route: string,
  method: 'GET'|'POST'|'PATCH'|'DELETE',
  data?: Record<string, any>
): Promise<Resp> {
  const req: Req = createReq(bffUrlBase + route, method, data)
  return await accessBackend(req)
}

async function accessProtectedBff(
  route: string,
  method: 'GET'|'POST'|'PATCH'|'DELETE',
  data?: Record<string, any>
): Promise<Resp> {
  let resp: Resp = await accessBff(route, method, data)
  if (resp.status === 401 && resp.data?.msg === 'Token has expired') {
    const refreshResp: Resp = await accessBff(bffAuthRoute + '/refresh', 'POST')
    if (refreshResp.status === 200) {
      resp = await accessBff(route, method, data)
    }
  }
  return resp
}

export {
  apiUrlBase, apiTokenRoute, apiUserRoute,
  bffUrlBase, bffAuthRoute, bffUserRoute,
  accessBackend, accessApi, accessBff, accessProtectedBff
}

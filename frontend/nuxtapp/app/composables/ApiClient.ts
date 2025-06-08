import {getJwt} from '~/composables/JwtManager'
import type {Resp} from '~/types'

const jwt_api_route: string = '/jwt/'
const user_api_route: string = '/user/'

function requestInit(
  method: string = 'GET', body?: any
): RequestInit {
  const init: RequestInit = {
    method: method,
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + getJwt()
    }
  }
  if (['POST', 'PATCH'].includes(method)) {
    init.body = JSON.stringify(body)
  }
  return init
}

async function apiRequest(
  route: string = '/', init: RequestInit = requestInit()
): Promise<Resp> {
  try {
    await new Promise(r => setTimeout(r, 500))  // アクセスによる遅延を再現
    const response: Response = await fetch(
      useRuntimeConfig().public.apiUrlBase + route, init
    )
    return {
      status: response.status,
      body: response.status === 204 ? '' : await response.json()
    }
  }
  catch(_) {
    return {
      status: 500,
      body: {'msg': 'API access failed'}
    }
  }
}

async function accessJwtPost(
  email: string, password: string
): Promise<Resp> {
  return apiRequest(
    jwt_api_route, requestInit(
      'POST', {
        email: email,
        password: password
      }
    )
  )
}

async function accessUserGet(): Promise<Resp> {
  return apiRequest(
    user_api_route, requestInit('GET')
  )
}

async function accessUserPost(
  email: string, password: string, name: string
): Promise<Resp> {
  return apiRequest(
    user_api_route, requestInit(
      'POST', {
        email: email, 
        password: password,
        name: name
      }
    )
  )
}

async function accessUserPatch(
  param: string, current_val: string, new_val: string
): Promise<Resp> {
  return apiRequest(
    user_api_route, requestInit(
      'PATCH', {
        param: param,
        current_val: current_val, 
        new_val: new_val
      }
    )
  )
}

async function accessUserDelete(): Promise<Resp> {
  return apiRequest(
    user_api_route, requestInit('DELETE')
  )
}

export {
  jwt_api_route, user_api_route,
  accessJwtPost,
  accessUserGet, accessUserPost, accessUserPatch, accessUserDelete
}

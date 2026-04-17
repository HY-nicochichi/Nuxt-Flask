import {getJwt} from '~/composables/JwtManager'
import type {Resp} from '~/types'

const jwt_route: string = '/jwt/'
const user_route: string = '/user/'

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
    await new Promise(r => setTimeout(r, 500))  // simulate network delay
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
    jwt_route, requestInit(
      'POST', {
        email: email,
        password: password
      }
    )
  )
}

async function accessUserGet(): Promise<Resp> {
  return apiRequest(
    user_route, requestInit('GET')
  )
}

async function accessUserPost(
  email: string, password: string, name: string
): Promise<Resp> {
  return apiRequest(
    user_route, requestInit(
      'POST', {
        email: email, 
        password: password,
        name: name
      }
    )
  )
}

async function accessUserPatch(
  body: Record<string, string>
): Promise<Resp> {
  return apiRequest(
    user_route, requestInit('PATCH', body)
  )
}

async function accessUserDelete(): Promise<Resp> {
  return apiRequest(
    user_route, requestInit('DELETE')
  )
}

export {
  jwt_route, user_route,
  accessJwtPost,
  accessUserGet, accessUserPost, accessUserPatch, accessUserDelete
}

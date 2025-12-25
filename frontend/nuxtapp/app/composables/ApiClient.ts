import {getJwt} from '~/composables/JwtManager'
import type {Resp} from '~/types'

const jwt_api_route: string = '/jwt/'
const user_api_route: string = '/user/'

function getOptions(): RequestInit {
  return {
    method: 'GET',
    mode: 'cors',
    headers: {
      'Authorization': 'Bearer ' + getJwt()
    }
  }
}

function postOptions(json: any): RequestInit {
  return {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + getJwt()
    },
    body: JSON.stringify(json)
  }
}

function patchOptions(json: any): RequestInit {
  return {
    method: 'PATCH',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + getJwt()
    },
    body: JSON.stringify(json)
  }
}

function deleteOptions(): RequestInit {
  return {
    method: 'DELETE',
    mode: 'cors',
    headers: {
      'Authorization': 'Bearer ' + getJwt()
    }
  }
}

async function apiRequest(
  route: string = '/',
  options: RequestInit = getOptions()
): Promise<Resp> {
  try {
    const response: Response = await fetch(
      'http://localhost:5000' + route, options
    )
    return {
      status: response.status,
      body: response.status === 204 ? '' : await response.json()
    }
  }
  catch(error) {
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
    jwt_api_route, postOptions({
      email: email,
      password: password
    })
  )
}

async function accessUserGet(): Promise<Resp> {
  return apiRequest(
    user_api_route, getOptions()
  )
}

async function accessUserPost(
  email: string, password: string, name: string
): Promise<Resp> {
  return apiRequest(
    user_api_route, postOptions({
      email: email, 
      password: password,
      name: name
    })
  )
}

async function accessUserPatch(
  param: string, current_val: string, new_val: string
): Promise<Resp> {
  return apiRequest(
    user_api_route, patchOptions({
      param: param,
      current_val: current_val, 
      new_val: new_val
    })
  )
}

async function accessUserDelete(): Promise<Resp> {
  return apiRequest(
    user_api_route, deleteOptions()
  )
}

export {
  accessJwtPost,
  accessUserGet, accessUserPost, accessUserPatch, accessUserDelete
}

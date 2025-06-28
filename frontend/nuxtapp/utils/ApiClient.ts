const api_domain: string = 'http://localhost:5000'
const jwt_api_route: string = api_domain + '/jwt/'
const user_api_route: string = api_domain + '/user/'

async function accessJwtPost(email: string, password: string): Promise<Resp> {
  const response: Response = await fetch(
    jwt_api_route, {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email,
        password: password
      })
    }
  )
  const resp: Resp = {
    status: response.status,
    json: await response.json()
  }
  return resp
}

async function accessUserGet(): Promise<Resp> {
  const response: Response = await fetch(
    user_api_route, {
      method: 'GET',
      mode: 'cors',
      headers: {
        'Authorization': 'Bearer ' + getJwt()
      }
    }
  )
  const resp: Resp = {
    status: response.status,
    json: await response.json()
  }
  return resp
}

async function accessUserPost(email: string, password: string, name: string): Promise<Resp> {
  const response: Response = await fetch(
    user_api_route, {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email, 
        password: password,
        name: name
      })
    }
  )
  const resp: Resp = {
    status: response.status,
    json: await response.json()
  }
  return resp
}

async function accessUserPut(param: string, current_val: string, new_val: string): Promise<Resp> {
  const response: Response = await fetch(
    user_api_route, {
      method: 'PUT',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + getJwt()
      },
      body: JSON.stringify({
        param: param,
        current_val: current_val, 
        new_val: new_val
      })
    }
  )
  const resp: Resp = {
    status: response.status,
    json: await response.json()
  }
  return resp
}

async function accessUserDelete(): Promise<Resp> {
  const response: Response = await fetch(
    user_api_route, {
      method: 'DELETE',
      mode: 'cors',
      headers: {
        'Authorization': 'Bearer ' + getJwt()
      }
    }
  )
  const resp: Resp = {
    status: response.status,
    json: await response.json()
  }
  return resp
}

export {
  accessJwtPost, accessUserGet, accessUserPost, accessUserPut, accessUserDelete
}

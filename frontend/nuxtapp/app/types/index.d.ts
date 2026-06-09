interface Req {
  route: string
  init: { 
    mode: 'cors'|'same-origin'
    credentials: 'omit'|'same-origin'
    headers: Record<string, string>
    method: 'GET'|'POST'|'PATCH'|'DELETE'
    body?: string
  }
}

interface Resp {
  status: ContentfulStatusCode
  body: any
}

interface User {
  login: boolean
  name: string
  email: string
}
  
interface Alert {
  show: boolean
  msg: string
}

interface Input {
  label: string
  type: string
  value: string
  validation: (val: string) => boolean
}

export type {
  Req, Resp, User, Alert, Input
}

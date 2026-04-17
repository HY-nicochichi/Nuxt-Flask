interface Resp {
  status: number
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
  Resp, User, Alert, Input
}

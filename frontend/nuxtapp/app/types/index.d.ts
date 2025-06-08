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

interface Validation {
  (val: string): boolean
}

interface Input {
  label: string
  type: string
  value: string
  validation: Validation
}

export type {
  Resp, User, Alert, Validation, Input
}

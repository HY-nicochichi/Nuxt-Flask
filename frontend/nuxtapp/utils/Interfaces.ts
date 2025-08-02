interface Resp {
  status: number
  json: any
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
  label: Ref<string>
  type: Ref<string>
  model: Ref<string>
}

interface Submit {
  name: string
  func: (e: MouseEvent) => void
}

export type {
  Resp, User, Alert, Input, Submit
}

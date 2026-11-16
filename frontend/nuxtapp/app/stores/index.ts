export const useAlertStore = defineStore('alert', () => {
  type Alert = {show: boolean, msg: string}
  const value: Ref<Alert> = ref({show: false, msg: ''})

  function show(msg: string): void {value.value = {show: true, msg: msg}}

  function clear(): void {value.value = {show: false, msg: ''}}

  return {value, show, clear}
})

export const useUserStore = defineStore('user', () => {
  type User = {login: boolean, name: string, email: string}
  const value: Ref<User> = ref({login: false, email: '', name: ''})

  function login(email: string, name: string): void {
    value.value = {login: true, email: email, name: name}
  }

  function clear(): void {value.value = {login: false, email: '', name: ''}}

  return {value, login, clear}
})

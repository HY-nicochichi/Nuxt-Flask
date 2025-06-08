import type {Alert, User} from '~/types'

const useAlertStore = defineStore('alert', () => {
  const value: Ref<Alert> = ref({
    show: false, msg: ''
  })

  function show(msg: string): void {
    value.value = {
      show: true, msg: msg
    }
  }

  function clear(): void {
    value.value = {
      show: false, msg: ''
    }
  }

  return {value, show, clear}
})

const useUserStore = defineStore('user', () => {
  const value: Ref<User> = ref({
    login: false, email: '', name: ''
  })

  function login(email: string, name: string): void {
    value.value = {
      login: true, email: email, name: name
    }
  }

  function clear(): void {
    value.value = {
      login: false, email: '', name: ''
    }
  }

  return {value, login, clear}
})

export {useAlertStore, useUserStore}

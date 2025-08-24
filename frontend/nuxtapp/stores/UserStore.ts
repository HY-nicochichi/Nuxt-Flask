export const useUserStore = defineStore('user', () => {
  const value: Ref<User> = ref({
    login: false, email: '', name: ''
  })

  function loginUser(email: string, name: string): void {
    value.value = {
      login: true, email: email, name: name
    }
  }

  function clear(): void {
    value.value = {
      login: false, email: '', name: ''
    }
  }

  return { value, loginUser, clear }
})

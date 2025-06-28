export const useUserStore = defineStore('user', () => {
  const value: Ref<User> = ref({
    login: false,
    email: '',
    name: ''
  })

  return { value }
})

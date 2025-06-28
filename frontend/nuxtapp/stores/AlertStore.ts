export const useAlertStore = defineStore('alert', () => {
  const value: Ref<Alert> = ref({
    show: false,
    msg: ''
  })

  return { value }
})

export const useAlertStore = defineStore('alert', () => {
  const value: Ref<Alert> = ref({
    show: false, msg: ''
  })

  function showMessage(msg: string): void {
    value.value = {
      show: true, msg: msg
    }
  }

  function clear(): void {
    value.value = {
      show: false, msg: ''
    }
  }

  return { value, showMessage, clear }
})

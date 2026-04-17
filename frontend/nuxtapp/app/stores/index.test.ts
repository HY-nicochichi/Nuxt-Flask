import {describe, it, expect, beforeEach} from 'vitest'
import {setActivePinia, createPinia} from 'pinia'
import {useAlertStore, useUserStore} from '~/stores/index'

describe('Stores', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  describe('useAlertStore', () => {
    it('Initial state', () => {
      const alert = useAlertStore()
      expect(alert.value).toEqual({
        show: false, msg: ''
      })
    })

    it('Show message', () => {
      const alert = useAlertStore()
      alert.show('test error message')
      expect(alert.value).toEqual({
        show: true, msg: 'test error message'
      })
    })

    it('Clear store', () => {
      const alert = useAlertStore()
      alert.show('Temp message')
      alert.clear()
      expect(alert.value).toEqual({
        show: false, msg: ''
      })
    })
  })

  describe('useUserStore', () => {
    it('Initial state', () => {
      const user = useUserStore()
      expect(user.value).toEqual({
        login: false, email: '', name: ''
      })
    })

    it('Login user', () => {
      const user = useUserStore()
      user.login('test@example.com', 'Taro')
      expect(user.value).toEqual({
        login: true, email: 'test@example.com', name: 'Taro'
      })
    })

    it('Clear store', () => {
      const user = useUserStore()
      user.login('test@example.com', 'Taro')
      user.clear()
      expect(user.value).toEqual({
        login: false, email: '', name: ''
      })
    })
  })
})

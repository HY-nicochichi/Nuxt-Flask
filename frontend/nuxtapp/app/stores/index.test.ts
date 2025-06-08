import {describe, it, expect, beforeEach} from 'vitest'
import {setActivePinia, createPinia} from 'pinia'
import {useAlertStore, useUserStore} from '~/stores/index'

describe('Stores', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  describe('useAlertStore', () => {
    it('初期状態', () => {
      const alert = useAlertStore()
      expect(alert.value).toEqual({
        show: false, msg: ''
      })
    })

    it('show でアラート文を保持', () => {
      const alert = useAlertStore()
      alert.show('test error message')
      expect(alert.value).toEqual({
        show: true, msg: 'test error message'
      })
    })

    it('clear でリセット', () => {
      const alert = useAlertStore()
      alert.show('Temp message')
      alert.clear()
      expect(alert.value).toEqual({
        show: false, msg: ''
      })
    })
  })

  describe('useUserStore', () => {
    it('初期状態', () => {
      const user = useUserStore()
      expect(user.value).toEqual({
        login: false, email: '', name: ''
      })
    })

    it('login ユーザー情報を保持', () => {
      const user = useUserStore()
      user.login('test@example.com', 'Taro')
      expect(user.value).toEqual({
        login: true, email: 'test@example.com', name: 'Taro'
      })
    })

    it('clear でリセット', () => {
      const user = useUserStore()
      user.login('test@example.com', 'Taro')
      user.clear()
      expect(user.value).toEqual({
        login: false, email: '', name: ''
      })
    })
  })
})

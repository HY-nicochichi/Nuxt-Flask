import {describe, it, expect, beforeEach} from 'vitest'
import {getJwt, setJwt} from '~/composables/JwtManager'

describe('JwtManager', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('初期状態', () => {
    expect(getJwt()).toBe('')
  })

  it('setJwt で保存した値を getJwt で取得', () => {
    setJwt('test.jwt.value')
    expect(getJwt()).toBe('test.jwt.value')
    expect(localStorage.getItem('JWT')).toBe('test.jwt.value')
  })

  it('setJwt に引数を渡さない', () => {
    setJwt()
    expect(getJwt()).toBe('')
    expect(localStorage.getItem('JWT')).toBe('')
  })
})

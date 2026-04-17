import {describe, it, expect, beforeEach} from 'vitest'
import {getJwt, setJwt} from '~/composables/JwtManager'

describe('JwtManager', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('Initial state', () => {
    expect(getJwt()).toBe('')
  })

  it('setJwt and getJwt', () => {
    setJwt('test.jwt.value')
    expect(getJwt()).toBe('test.jwt.value')
    expect(localStorage.getItem('JWT')).toBe('test.jwt.value')
  })

  it('setJwt with no args', () => {
    setJwt()
    expect(getJwt()).toBe('')
    expect(localStorage.getItem('JWT')).toBe('')
  })
})

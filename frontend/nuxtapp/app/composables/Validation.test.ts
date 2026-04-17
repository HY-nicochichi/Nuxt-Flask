import {describe, it, expect} from 'vitest'
import {validateEmail, validatePassword, validateName} from '~/composables/Validation'

describe('Validation', () => {

  describe('validateEmail', () => {
    it('Valid email', () => {
      expect(validateEmail('test@email.com')).toBe(true)
    })

    it('Invalid email length', () => {
      expect(validateEmail('a@b.com')).toBe(false)
      expect(validateEmail('a'.repeat(41) + '@email.com')).toBe(false)
    })

    it('Invalid email format', () => {
      expect(validateEmail('test-email.com')).toBe(false)
      expect(validateEmail('test@emailcom')).toBe(false)
      expect(validateEmail('@email.com')).toBe(false)
    })
  })

  describe('validatePassword', () => {
    it('Valid password', () => {
      expect(validatePassword('Test1234')).toBe(true)
    })

    it('Invalid password length', () => {
      expect(validatePassword('Test123')).toBe(false)
      expect(validatePassword('A' + 'a'.repeat(20))).toBe(false)
    })

    it('Invalid password format', () => {
      expect(validatePassword('test1234')).toBe(false)
      expect(validatePassword('TEST1234')).toBe(false)
      expect(validatePassword('TestTest')).toBe(false)
      expect(validatePassword('Test1234!')).toBe(false)
    })
  })

  describe('validateName', () => {
    it('Valid name', () => {
      expect(validateName('Test')).toBe(true)
    })

    it('Invalid name length', () => {
      expect(validateName('')).toBe(false)
      expect(validateName('A'.repeat(31))).toBe(false)
    })
  })
})

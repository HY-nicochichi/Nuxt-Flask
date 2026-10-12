import {describe, it, expect} from 'vitest'
import {validateEmail, validatePassword, validateName} from '~/composables/Validation'

describe('Validation', () => {

  describe('validateEmail', () => {
    it('Valid email', () => {
      expect(validateEmail('test@email.com')).toBe(true)
    })

    it('Invalid email length', () => {
      expect(validateEmail('a'.repeat(91) + '@email.com')).toBe(false)
    })

    it('Invalid email format', () => {
      expect(validateEmail('test-email.com')).toBe(false)
      expect(validateEmail('test@emailcom')).toBe(false)
      expect(validateEmail('@email.com')).toBe(false)
    })
  })

  describe('validatePassword', () => {
    it('Valid password', () => {
      expect(validatePassword('TestPassword123')).toBe(true)
      expect(validatePassword('test_password_123!')).toBe(true)
    })

    it('Invalid password length', () => {
      expect(validatePassword('Test' + '0'.repeat(10))).toBe(false)
      expect(validatePassword('Test' + '0'.repeat(72))).toBe(false)
    })

    it('Invalid password format', () => {
      expect(validatePassword('LetterOnlyPassword')).toBe(false)
      expect(validatePassword('0'.repeat(15))).toBe(false)
      expect(validatePassword('Test Password 123')).toBe(false)
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

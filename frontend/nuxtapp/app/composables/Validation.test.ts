import {describe, it, expect} from 'vitest'
import { 
  validateEmail, validatePassword, validateName, validateEmpty,
  selectValidation
} from '~/composables/Validation'

describe('Validation', () => {

  describe('validateEmail', () => {
    it('正常なメールアドレス', () => {
      expect(validateEmail('test@email.com')).toBe(true)
    })

    it('10文字未満または51文字以上', () => {
      expect(validateEmail('a@b.com')).toBe(false)
      expect(validateEmail('a'.repeat(41) + '@email.com')).toBe(false)
    })

    it('不正な形式', () => {
      expect(validateEmail('test-email.com')).toBe(false)
      expect(validateEmail('test@emailcom')).toBe(false)
      expect(validateEmail('@email.com')).toBe(false)
    })
  })

  describe('validatePassword', () => {
    it('正常なパスワード', () => {
      expect(validatePassword('Test1234')).toBe(true)
    })

    it('8文字未満または21文字以上', () => {
      expect(validatePassword('Test123')).toBe(false)
      expect(validatePassword('A' + 'a'.repeat(20))).toBe(false)
    })

    it('不正な形式', () => {
      expect(validatePassword('test1234')).toBe(false)
      expect(validatePassword('TEST1234')).toBe(false)
      expect(validatePassword('TestTest')).toBe(false)
      expect(validatePassword('Test1234!')).toBe(false)
    })
  })

  describe('validateName', () => {
    it('正常な名前', () => {
      expect(validateName('Test')).toBe(true)
    })

    it('空文字または31文字以上は失敗', () => {
      expect(validateName('')).toBe(false)
      expect(validateName('A'.repeat(31))).toBe(false)
    })
  })

  describe('validateEmpty', () => {
    it('空でなければ true, 空なら false', () => {
      expect(validateEmpty('not empty')).toBe(true)
      expect(validateEmpty('')).toBe(false)
    })
  })

  describe('selectValidation', () => {
    it('正しい関数を返す', () => {
      expect(selectValidation('email')).toBe(validateEmail)
      expect(selectValidation('password')).toBe(validatePassword)
      expect(selectValidation('name')).toBe(validateName)
      expect(selectValidation('unknown')).toBe(validateEmpty)
    })
  })
})

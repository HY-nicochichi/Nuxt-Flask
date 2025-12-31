import type {Validation} from '~/types'

function validateEmail(val: string): boolean {
  return /^(?=.{10,50}$)[a-z0-9.-]+@[a-z0-9-]+\.[a-z0-9.-]+$/.test(val)
}

function validatePassword(val: string): boolean {
  return /^(?=.{8,20}$)(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[a-zA-Z0-9]+$/.test(val)
}

function validateName(val: string): boolean {
  return /^.{1,30}$/.test(val)
}

function validateEmpty(val: string): boolean {
  return val !== ''
}

function selectValidation(type: string): Validation {
  switch (type) {
    case 'email':
      return validateEmail
    case 'password':
      return validatePassword
    case 'name':
      return validateName
    default:
      return validateEmpty
  }
}

export {
  validateEmail, validatePassword, validateName, validateEmpty,
  selectValidation
}

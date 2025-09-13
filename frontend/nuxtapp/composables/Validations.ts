function validateEmail(val: string): boolean {
  return /^(?=.{10,32}$)[a-z0-9.-]+@[a-z0-9-]+\.[a-z0-9.-]+$/.test(val)
}
function validatePassword(val: string): boolean {
  return /^(?=.{8,16}$)(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[a-zA-Z0-9]+$/.test(val)
}

function validateName(val: string) {
  return /^.{1,16}$/.test(val)
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

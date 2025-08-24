function validateEmail(val: string): boolean {
  const split = val.split('@')
  return split.length === 2 && split[0] !== '' && split[1] !== '' && val.length >= 8 && val.length <= 32
}

function validatePassword(val: string): boolean {
  return /[a-zA-Z]/.test(val) && /[0-9]/.test(val) && val.length >= 8 && val.length <= 16
}

function validateName(val: string) {
  return val !== '' && val.length <= 16
}

function validateEmpty(val: string): boolean {
  return val !== ''
}

function selectValidation(type: string): Validation {
  if (type === 'email') {
    return validateEmail
  }
  else if (type === 'password') {
    return validatePassword
  }
  else if (type === 'name') {
    return validateName
  }  
  else {
    return validateEmpty
  }
}

export {
  validateEmail, validatePassword, validateName, validateEmpty,
  selectValidation
}

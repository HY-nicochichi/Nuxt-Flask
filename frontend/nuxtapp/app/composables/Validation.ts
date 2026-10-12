function validateEmail(val: string): boolean {
  return /^(?=.{6,100}$)[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(val)
}

function validatePassword(val: string): boolean {
  return /^(?=.{15,75}$)(?=.*[a-zA-Z])(?=.*[0-9])[\x21-\x7E]+$/.test(val)
}

function validateName(val: string): boolean {
  return /^.{1,30}$/.test(val)
}

export {
  validateEmail, validatePassword, validateName
}

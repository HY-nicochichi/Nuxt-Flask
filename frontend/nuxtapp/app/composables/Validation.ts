function validateEmail(val: string): boolean {
  return /^(?=.{10,50}$)[a-z0-9.-]+@[a-z0-9-]+\.[a-z0-9.-]+$/.test(val)
}

function validatePassword(val: string): boolean {
  return /^(?=.{8,20}$)(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[a-zA-Z0-9]+$/.test(val)
}

function validateName(val: string): boolean {
  return /^.{1,30}$/.test(val)
}

export {
  validateEmail, validatePassword, validateName
}

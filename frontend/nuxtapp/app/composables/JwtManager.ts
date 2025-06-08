function getJwt(): string {
  return localStorage.getItem('JWT') ?? ''
}

function setJwt(jwt: string = ''): void {
  localStorage.setItem('JWT', jwt)
}

export {
  getJwt, setJwt
}

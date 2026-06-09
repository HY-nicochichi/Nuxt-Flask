import crypto from 'node:crypto'

const ALGORITHM = 'aes-256-gcm'
const KEY = crypto.createHash('sha256').update(process.env.BFF_COOKIE_SECRET as string).digest()

function encryptToken(text: string): string {
  const iv = crypto.randomBytes(12)
  const cipher = crypto.createCipheriv(ALGORITHM, KEY, iv)
  const encrypted = Buffer.concat([cipher.update(text, 'utf8'), cipher.final()])
  const tag = cipher.getAuthTag()
  return Buffer.concat([iv, tag, encrypted]).toString('hex')
}

function decryptToken(encryptedHex?: string): string|undefined {
  try {
    if (!encryptedHex) throw new Error('No encrypted token')
    const buffer = Buffer.from(encryptedHex, 'hex')
    const iv = buffer.subarray(0, 12)
    const tag = buffer.subarray(12, 28)
    const encrypted = buffer.subarray(28)
    const decipher = crypto.createDecipheriv(ALGORITHM, KEY, iv)
    decipher.setAuthTag(tag)
    return decipher.update(encrypted).toString('utf8') + decipher.final('utf8')
  } catch {
    return undefined
  }
}

export {encryptToken, decryptToken}

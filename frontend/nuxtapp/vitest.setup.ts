import {vi} from 'vitest'

globalThis.fetch = vi.fn()

globalThis.localStorage = {
  getItem: vi.fn(
    (key: string) => {
      return process.env[`TEST_STORAGE_${key}`] ?? null
    }
  ),
  setItem: vi.fn(
    (key: string, val: string) => {
      process.env[`TEST_STORAGE_${key}`] = val
    }
  ),
  clear: vi.fn(
    () => {
      Object.keys(process.env).forEach((key) => {
        if (key.startsWith('TEST_STORAGE_')) {
          delete process.env[key]
        }
      })
    }
  )
}

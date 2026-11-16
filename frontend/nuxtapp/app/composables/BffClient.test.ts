import {describe, it, expect, vi, beforeEach} from 'vitest'
import {bffAuthRoute, bffUserRoute} from '#shared'
import {accessBff, accessProtectedBff} from '~/composables/BffClient'

describe('BffClient', () => {
  function mockFetchResult(status: number, json?: any): void {
    vi.mocked(fetch).mockImplementationOnce(
      async() => Response.json(json, {status: status})
    )
  }

  beforeEach(() => {
    vi.useFakeTimers()
    vi.clearAllMocks()
    globalThis.fetch = vi.fn()
  })

  it('Access failed', async() => {
    vi.mocked(fetch).mockRejectedValue(new Error('Network Error'))
    const promiseRes = accessBff('/not-accessible', 'GET')
    await vi.advanceTimersByTimeAsync(300)
    expect(await promiseRes).toEqual({
      status: 500, data: {msg: 'Unexpected error in network or server'}
    })
  })

  it('Access BFF', async() => {
    mockFetchResult(200, {msg: 'Logged in successfully'})
    const promiseRes = accessBff(
      bffAuthRoute + '/login', 'POST', {
        email: 'test@email.com', password: 'TestPassword123'
      }
    )
    await vi.advanceTimersByTimeAsync(300)
    expect(await promiseRes).toEqual({
      status: 200, data: {msg: 'Logged in successfully'}
    })
  })

  it('Access protected BFF', async() => {
    mockFetchResult(200, {email: 'test@email.com', name: 'Test'})
    const promiseResNormal = accessProtectedBff(bffUserRoute + '/me', 'GET')
    await vi.advanceTimersByTimeAsync(300) 
    expect(await promiseResNormal).toEqual({
      status: 200, data: {email: 'test@email.com', name: 'Test'}
    })
    expect(fetch).toHaveBeenCalledTimes(1)
    vi.clearAllMocks()
    mockFetchResult(401, {msg: 'Token has expired'})
    mockFetchResult(200, {msg: 'Refreshed successfully'})
    mockFetchResult(200, {email: 'test@email.com', name: 'Test'})
    const promiseResRetry = accessProtectedBff(bffUserRoute + '/me', 'GET')
    await vi.advanceTimersByTimeAsync(3*300)
    expect(await promiseResRetry).toEqual({
      status: 200, data: {email: 'test@email.com', name: 'Test'}
    })
    expect(fetch).toHaveBeenCalledTimes(3)
  })
})

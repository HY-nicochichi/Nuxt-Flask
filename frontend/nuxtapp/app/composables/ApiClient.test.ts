import {describe, it, expect, vi, beforeEach} from 'vitest'
import {
  apiUrlBase, apiUserRoute,
  bffUrlBase, bffAuthRoute, bffUserRoute,
  accessBackend, accessApi, accessBff, accessProtectedBff
} from '~/composables/ApiClient'

describe('ApiClient', () => {
  function testFetchResult(status: number, json?: any): void {
    vi.mocked(fetch).mockResolvedValue(
      {status, json: async() => json} as Response
    )
  }

  beforeEach(() => {
    vi.useFakeTimers()
    vi.clearAllMocks()
    globalThis.fetch = vi.fn()
  })

  it('Access failed', async() => {
    vi.mocked(fetch).mockRejectedValue(new Error('Network Error'))
    const promiseResp = accessBackend({
      route: '/not-accessible', init: {
        method: 'GET', credentials: 'omit', headers: {}
      }
    })
    await vi.advanceTimersByTimeAsync(300)
    const resp = await promiseResp
    expect(resp.status).toBe(500)
    expect(resp.data).toEqual({msg: 'Unexpected error in network or server'})
  })

  it('Access API', async() => {
    testFetchResult(200, {email: 'test@email.com', password: 'Test1234'})
    const promiseResp = accessApi(
      apiUserRoute + '/me', 'GET', undefined, 'test.jwt.value'
    )
    await vi.advanceTimersByTimeAsync(300)
    const resp = await promiseResp
    expect(resp.status).toBe(200)
    expect(resp.data).toEqual({email: 'test@email.com', password: 'Test1234'})
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining(apiUrlBase + apiUserRoute + '/me'),
      expect.objectContaining({
        method: 'GET',
        credentials: 'omit',
        headers: {'Authorization': 'Bearer test.jwt.value'}
      })
    )
  })

  it('Access BFF', async() => {
    testFetchResult(200, {msg: 'Logged in successfully'})
    const promiseResp = accessBff(
      bffAuthRoute + '/login', 'POST',
      {email: 'test@email.com', password: 'Test1234'}
    )
    await vi.advanceTimersByTimeAsync(300)
    const resp = await promiseResp
    expect(resp.status).toBe(200)
    expect(resp.data).toEqual({msg: 'Logged in successfully'})
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining(bffUrlBase + bffAuthRoute + '/login'),
      expect.objectContaining({
        method: 'POST',
        credentials: 'same-origin',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          email: 'test@email.com', password: 'Test1234'
        })
      })
    )
  })

  it('Access protected BFF', async() => {
    testFetchResult(200, {email: 'test@email.com', name: 'Test'})
    const promiseRespNormal = accessProtectedBff(bffUserRoute + '/me', 'GET')
    await vi.advanceTimersByTimeAsync(300) 
    const respNormal = await promiseRespNormal
    expect(respNormal.status).toBe(200)
    expect(respNormal.data).toEqual({email: 'test@email.com', name: 'Test'})
    expect(fetch).toHaveBeenCalledTimes(1)
    vi.clearAllMocks()
    vi.mocked(fetch)
      .mockImplementationOnce(async() => ({
        status: 401,
        json: async() => ({msg: 'Token has expired'})
      } as Response))
      .mockImplementationOnce(async() => ({
        status: 200,
        json: async() => ({msg: 'Refreshed successfully'})
      } as Response))
      .mockImplementationOnce(async() => ({
        status: 200,
        json: async() => ({email: 'test@email.com', name: 'Test'})
      } as Response))
    const promiseRespRetry = accessProtectedBff(bffUserRoute + '/me', 'GET')
    await vi.advanceTimersByTimeAsync(900)
    const respRetry = await promiseRespRetry
    expect(respRetry.status).toBe(200)
    expect(respRetry.data).toEqual({email: 'test@email.com', name: 'Test'})
    expect(fetch).toHaveBeenCalledTimes(3)
    expect(fetch).toHaveBeenNthCalledWith(
      2,
      expect.stringContaining(bffUrlBase + bffAuthRoute + '/refresh'),
      expect.objectContaining({method: 'POST'})
    )
  })
})

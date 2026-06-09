import {describe, it, expect, vi, beforeEach} from 'vitest'
import {
  api_user_route, bff_auth_route,
  accessBackend, accessApi, accessBff
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
        method: 'GET', mode: 'cors', credentials: 'omit', headers: {}
      }
    })
    vi.advanceTimersByTime(300)
    const resp = await promiseResp
    expect(resp.status).toBe(500)
    expect(resp.body).toEqual({msg: 'Unexpected error in network or server'})
  })

  it('Access API', async() => {
    testFetchResult(200, {email: 'test@email.com', password: 'Test'})
    const promiseResp = accessApi(
      api_user_route, 'GET', undefined, 'test.jwt.value'
    )
    vi.advanceTimersByTime(300)
    const resp = await promiseResp
    expect(resp.status).toBe(200)
    expect(resp.body).toEqual({email: 'test@email.com', password: 'Test'})
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/test-api' + api_user_route),
      expect.objectContaining({
        method: 'GET',
        mode: 'cors',
        credentials: 'omit',
        headers: {'Authorization': 'Bearer test.jwt.value'}
      })
    )
  })

  it('Access BFF', async() => {
    testFetchResult(200, {msg: 'Logged in successfully'})
    const promiseResp = accessBff(
      bff_auth_route + 'login', 'POST',
      {email: 'test@email.com', password: 'Test1234'}
    )
    vi.advanceTimersByTime(300)
    const resp = await promiseResp
    expect(resp.status).toBe(200)
    expect(resp.body).toEqual({msg: 'Logged in successfully'})
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/bff' + bff_auth_route + 'login'),
      expect.objectContaining({
        method: 'POST',
        mode: 'same-origin',
        credentials: 'same-origin',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          email: 'test@email.com', password: 'Test1234'
        })
      })
    )
  })
})

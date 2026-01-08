import {describe, it, expect, vi, beforeEach} from 'vitest'
import {
  jwt_api_route, user_api_route,
  accessJwtPost,
  accessUserGet, accessUserPost, accessUserPatch, accessUserDelete
} from '~/composables/ApiClient'
import {setJwt} from '~/composables/JwtManager'

describe('ApiClient', () => {
  function testFetch(status: number, json: any = null): void {
    vi.mocked(fetch).mockResolvedValue(
      {status, json: async() => json} as Response
    )
  }

  beforeEach(() => {
    vi.useFakeTimers()
    vi.clearAllMocks()
    setJwt()
  })

  it('アクセスエラー', async() => {
    vi.mocked(fetch).mockRejectedValue(new Error('Network Error'))
    const promiseResp = accessUserGet()
    vi.advanceTimersByTime(500)
    const resp = await promiseResp
    expect(resp.status).toBe(500)
    expect(resp.body).toEqual({msg: 'API access failed'})
  })

  it('accessJwtPost', async() => {
    testFetch(200, {access_token: 'test.jwt.value'})
    const promiseResp = accessJwtPost('test@email.com', 'Test1234')
    vi.advanceTimersByTime(500)
    const resp = await promiseResp
    expect(resp.status).toBe(200)
    expect(resp.body).toEqual({access_token: 'test.jwt.value'})
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining(jwt_api_route),
      expect.objectContaining({
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer '
        },
        body: JSON.stringify({
          email: 'test@email.com',
          password: 'Test1234'
        })
      })
    )
  })

  it('accessUserGet', async() => {
    setJwt('test.jwt.value')
    testFetch(200, {email: 'test@email.com', name: 'Test'})
    const promiseResp = accessUserGet()
    vi.advanceTimersByTime(500)
    const resp = await promiseResp
    expect(resp.status).toBe(200)
    expect(resp.body).toEqual({email: 'test@email.com', name: 'Test'})
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining(user_api_route),
      expect.objectContaining({
        method: 'GET',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer test.jwt.value'
        }
      })
    )
  })

  it('accessUserPost', async() => {
    testFetch(201, {msg: 'Success'})
    const promiseResp = accessUserPost('test@email.com', 'Test1234', 'Test')
    vi.advanceTimersByTime(500)
    const resp = await promiseResp
    expect(resp.status).toBe(201)
    expect(resp.body).toEqual({msg: 'Success'})
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining(user_api_route),
      expect.objectContaining({
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer '
        },
        body: JSON.stringify({
          email: 'test@email.com',
          password: 'Test1234',
          name: 'Test'
        })
      })
    )
  })

  it('accessUserPatch', async() => {
    setJwt('test.jwt.value')
    testFetch(200, {msg: 'Success'})
    const promiseResp = accessUserPatch('name', 'Test', 'test')
    vi.advanceTimersByTime(500)
    const resp = await promiseResp
    expect(resp.status).toBe(200)
    expect(resp.body).toEqual({msg: 'Success'})
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining(user_api_route),
      expect.objectContaining({
        method: 'PATCH',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer test.jwt.value'
        },
        body: JSON.stringify({
          param: 'name',
          current_val: 'Test',
          new_val: 'test'
        })
      })
    )
  })

  it('accessUserDelete', async() => {
    setJwt('test.jwt.value')
    testFetch(204)
    const promiseResp = accessUserDelete()
    vi.advanceTimersByTime(500)
    const resp = await promiseResp
    expect(resp.status).toBe(204)
    expect(resp.body).toBe('')
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining(user_api_route),
      expect.objectContaining({
        method: 'DELETE',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer test.jwt.value'
        }
      })
    )
  })
})

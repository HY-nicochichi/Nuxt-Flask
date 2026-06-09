import {describe, it, expect, vi, beforeEach} from 'vitest'
import {mountSuspended, mockNuxtImport} from '@nuxt/test-utils/runtime'
import {nextTick} from 'vue'
import {useUserStore} from '~/stores'
import NavBar from '~/components/NavBar.vue'

let mockRoute: {name: string} = {name: 'index'}

mockNuxtImport('useRoute', () => {
  return () => mockRoute
})

let mockBackendStatus = 200
let mockBackendBody: any = {msg: 'Logged out successfully'}

mockNuxtImport('accessBff', () => {
  return async () => {
    return {
      status: mockBackendStatus,
      body: mockBackendBody
    }
  }
})

describe('NavBar', () => {
  const router = useRouter()
  const user = useUserStore()

  async function navBar(routeName: string = 'index') {
    mockRoute.name = routeName
    user.clear()
    const self = await mountSuspended(NavBar)
    return {
      self,
      elements: () => {
        return {links: self.findAll('a')}
      }
    }
  }

  beforeEach(() => {
    vi.clearAllMocks()
    mockBackendStatus = 200
    mockBackendBody = {msg: 'Logged out successfully'}
  })

  it('When not logged in', async() => {
    const {elements} = await navBar()
    expect(elements().links[0]!.text()).toContain('Nuxt-Flask')
    expect(elements().links[1]!.text()).toContain('login')
    expect(elements().links[2]!.text()).toContain('new user')
  })

  it('When logged in', async() => {
    const {elements} = await navBar()
    user.login('test@email.com', 'Test')
    await nextTick()
    expect(elements().links[1]!.text()).toContain('Test')
    expect(elements().links[2]!.text()).toContain('logout')
  })

  it('Logout in /index', async() => {
    const {elements} = await navBar('index')
    user.login('test@email.com', 'Test')
    await nextTick()
    const routerGoSpy = vi.spyOn(router, 'go')
    await elements().links[2]!.trigger('click')
    await nextTick()
    expect(routerGoSpy).toHaveBeenCalledWith(0)
  })

  it('Logout not in /index', async() => {
    const {elements} = await navBar('user-info')
    user.login('test@email.com', 'Test')
    await nextTick()
    const routerPushSpy = vi.spyOn(router, 'push')
    await elements().links[2]!.trigger('click')
    await nextTick()
    expect(routerPushSpy).toHaveBeenCalledWith({name: 'index'})
  })
})

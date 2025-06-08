import {describe, it, expect, vi} from 'vitest'
import {mountSuspended, mockNuxtImport} from '@nuxt/test-utils/runtime'
import NavBar from '~/components/NavBar.vue'
import {getJwt, setJwt} from '~/composables/JwtManager'
import {useUserStore} from '~/stores'

let mockRoute: {name: string} = {name: 'index'}

mockNuxtImport('useRoute', () => {
  return () => mockRoute
})

describe('NavBar', () => {
  const router = useRouter()
  const user = useUserStore()

  function testLogin() {
    setJwt('test.jwt.value')
    user.login('test@email.com', 'Test')
  }

  async function navBar(routeName: string = 'index') {
    mockRoute.name = routeName
    user.clear()
    setJwt()
    const self = await mountSuspended(
      NavBar, {route: mockRoute}
    )
    return {
      self,
      elements: () => {
        return {links: self.findAll('a')}
      }
    }
  }

  it('未ログイン状態', async() => {
    const {elements} = await navBar()
    expect(getJwt()).toBe('')
    expect(elements().links[0]!.text()).toContain('Nuxt-Flask')
    expect(elements().links[1]!.text()).toContain('login')
    expect(elements().links[2]!.text()).toContain('new user')
  })

  it('ログイン状態', async() => {
    const {elements} = await navBar()
    testLogin()
    await nextTick()
    expect(getJwt()).not.toBe('')
    expect(elements().links[1]!.text()).toContain('Test')
    expect(elements().links[2]!.text()).toContain('logout')
  })

  it('/index でのログアウト', async() => {
    const {elements} = await navBar()
    testLogin()
    await nextTick()
    const routerGoSpy = vi.spyOn(router, 'go')
    await elements().links[2]!.trigger('click')
    expect(getJwt()).toBe('')
    expect(routerGoSpy).toHaveBeenCalledWith(0)
  })

  it('/index 以外でのログアウト', async() => {
    const {elements} = await navBar('user-info')
    testLogin()
    await nextTick()
    const routerPushSpy = vi.spyOn(router, 'push')
    await elements().links[2]!.trigger('click')
    expect(routerPushSpy).toHaveBeenCalledWith({name: 'index'})
  })
})

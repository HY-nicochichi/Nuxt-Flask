import {describe, it, expect} from 'vitest'
import {mountSuspended} from '@nuxt/test-utils/runtime'
import AlertBox from '~/components/AlertBox.vue'
import {useAlertStore} from '~/stores'

describe('AlertBox', () => {
  const alert = useAlertStore()

  async function alertBox() {
    alert.clear()
    const self = await mountSuspended(
      AlertBox, {}
    )
    return {
      self,
      elements: () => {
        return {alert: self.find('div')}
      }
    }
  }

  it('初期状態', async() => {
    const {elements} = await alertBox()
    expect(elements().alert.exists()).toBe(false)
  })

  it('メッセージの表示', async() => {
    const {elements} = await alertBox()
    alert.show('test error message')
    await nextTick()
    expect(elements().alert.text()).toContain('※ test error message')
  })
})

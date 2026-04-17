import {mountSuspended} from '@nuxt/test-utils/runtime'
import {describe, it, expect} from 'vitest'
import {LoadingSpinner} from './SvgIcons'
import SubmitButton from '~/components/SubmitButton.vue'

describe('SubmitButton', () => {
  async function submitButton(invalid: boolean = false, submitting: boolean = false) {
    const clickFunc = async() => {
      await self.setProps({submitting: true})
      await new Promise(resolve => setTimeout(resolve, 10))
      await self.setProps({submitting: false})
    }
    const self = await mountSuspended(
      SubmitButton, {
        props: {
          invalid: invalid, submitting: submitting, click: clickFunc
        }
      }
    )
    return {
      self,
      elements: () => ({
        button: self.find('button'),
        spinner: () => self.findComponent(LoadingSpinner)
      })
    }
  }

  it('Initial state', async() => {
    const {elements} = await submitButton()
    expect(elements().button.text()).toContain('submit')
    expect(elements().button.element.disabled).toBe(false)
    expect(elements().spinner().exists()).toBe(false)
  })

  it('Validation error', async() => {
    const {elements} = await submitButton(true)
    expect(elements().button.element.disabled).toBe(true)
  })

  it('Submittion executed', async () => {
    const {elements} = await submitButton()
    elements().button.trigger('click')
    await nextTick()
    expect(elements().button.element.disabled).toBe(true)
    expect(elements().spinner().exists()).toBe(true)
    await new Promise(resolve => setTimeout(resolve, 10))
    await nextTick()
    expect(elements().button.element.disabled).toBe(false)
    expect(elements().button.text()).toContain('submit')
    expect(elements().spinner().exists()).toBe(false)
  })
})

import {describe, it, expect} from 'vitest'
import {mountSuspended} from '@nuxt/test-utils/runtime'
import InputField from '~/components/InputField.vue'

describe('InputField', () => {
  async function inputField(label: string, type: string, value: string = '') {
    const self = await mountSuspended(InputField, {
      props: {
        label: label, type: type, modelValue: value, 
        'onUpdate:modelValue': (value: string) => self.setProps({modelValue: value})
      }
    })
    return {
      self,
      elements: () => {
        return {
          label: self.find('label'), input: self.find('input')
        }
      }
    }
  }

  it('Initial state', async() => {
    const {elements} = await inputField('email', 'text')
    expect(elements().label.text()).toContain('email')
    expect((elements().input.element as HTMLInputElement).value).toBe('')
  })

  it('Input valid value', async() => {
    const {self, elements} = await inputField('email', 'text')
    await elements().input.setValue('taro@email.com')
    expect(self.emitted('update:modelValue')![0]![0]).toEqual('taro@email.com')
  })
})

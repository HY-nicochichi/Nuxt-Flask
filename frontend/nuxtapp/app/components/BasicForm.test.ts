import {describe, it, expect} from 'vitest'
import {mountSuspended} from '@nuxt/test-utils/runtime'
import BasicForm from '~/components/BasicForm.vue'
import {LoadingSpinner} from '~/components/SvgIcons'
import {validateEmpty} from '~/composables/Validation'
import type {Input} from '~/types'

describe('BasicForm', () => {
  function testProps(
    inputsValues: string[] = ['', '']
  ): {inputs: Input[]} {
    return {
      inputs: [
        {
          label: 'test-label-0',
          type: 'text',
          value: inputsValues[0]!,
          validation: validateEmpty
        },
        {
          label: 'test-label-1',
          type: 'text',
          value: inputsValues[1]!,
          validation: validateEmpty
        }
      ]
    }
  }

  async function basicForm() {
    const self = await mountSuspended(
      BasicForm, {props: testProps()}
    )
    return {
      self,
      elements: () => {
        return {
          labels: self.findAll('label'),
          inputs: self.findAll('input'),
          button: self.find('button')
        }
      }
    }
  }

  it('初期状態', async() => {
    const {elements} = await basicForm()
    expect(elements().labels[0]!.text()).toContain('test-label-0')
    expect(elements().labels[1]!.text()).toContain('test-label-1')
    expect(elements().button.text()).toContain('submit')
    expect(elements().button.element.disabled).toBe(true)
  })

  it('有効値の入力', async() => {
    const {self, elements} = await basicForm()
    await elements().inputs[0]!.setValue('test-value-0')
    await elements().inputs[1]!.setValue('test-value-1')
    expect(self.emitted('update')![0]).toEqual([0, 'test-value-0'])
    expect(self.emitted('update')![1]).toEqual([1, 'test-value-1'])
    await self.setProps(testProps(['test-value-0', 'test-value-1']))
    await nextTick()
    expect(elements().button.element.disabled).toBe(false)
  })

  it('送信処理の実行', async () => {
    const {self, elements} = await basicForm()
    await self.setProps(testProps(['test-value-0', 'test-value-1']))
    await elements().button.trigger('click')
    await nextTick()
    expect(elements().button.element.disabled).toBe(true)
    expect(self.findComponent(LoadingSpinner).exists()).toBe(true)
    const submitFunc = self.emitted('submit')![0]![0] as Function
    submitFunc()
    await nextTick()
    expect(elements().button.element.disabled).toBe(false)
    expect(elements().button.text()).toContain('submit')
  })
})

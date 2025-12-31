<script setup lang="ts">
  import AlertBox from '~/components/AlertBox.vue'
  import BasicForm from '~/components/BasicForm.vue'
  import {accessUserPatch} from '~/composables/ApiClient'
  import {selectValidation} from '~/composables/Validation'
  import {useAlertStore} from '~/stores'
  import type {Input, Resp} from '~/types'

  const route = useRoute()
  const router = useRouter()
  const alert = useAlertStore()

  const param: string = route.params.param as string ?? ''

  if (!['email', 'password', 'name'].includes(param)) {
    router.push('/404')
  }

  useHead({title: 'update ' + param})

  const type: string = param === 'password' ? 'password' : 'text'

  const inputValues: Ref<string[]> = ref(['', ''])

  function setInputValue(index: number, value: string): void {
    inputValues.value[index] = value
  }

  const inputs: ComputedRef<Input[]> = computed(() => [
    {
      label: 'current ' + param,
      type: type,
      value: inputValues.value[0] ?? '',
      validation: selectValidation(param)
    },
    {
      label: 'new ' + param,
      type: type,
      value: inputValues.value[1] ?? '',
      validation: selectValidation(param)
    }
  ])

  async function updateUser(done: () => void): Promise<void> {
    const resp: Resp = await accessUserPatch(
      param, inputs.value[0]?.value ?? '', inputs.value[1]?.value ?? ''
    )
    if (resp.status === 200) {
      router.push({name: 'user-info'})
    }
    else {
      alert.show(resp.body.msg)
      done()
    }
  }
</script>


<template>
  <AlertBox/>
  <h4 class="fw-bolder mb-3">update {{ param }}</h4>
  <BasicForm
    :inputs="inputs"
    @update="setInputValue"
    @submit="updateUser"
  />
</template>

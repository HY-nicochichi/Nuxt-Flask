<script setup lang="ts">
  const router = useRouter()
  const route = useRoute()
  const alert = useAlertStore()

  const GoodParams: string[] = [
    'email', 'password', 'name'
  ]

  const param: Ref<string> = ref(route.params.param as string ?? '')

  const current_val: Input = {
    label: ref('current ' + param.value),
    type: ref('text'),
    model: ref('')
  }
  const new_val: Input = {
    label: ref('new ' + param.value),
    type: ref('text'),
    model: ref('')
  }

  async function tryUpdateUser(): Promise<void> {
    if (current_val.model.value === '' || new_val.model.value === '') {
      alert.value = {
        show: true,
        msg: 'Fill all input fields'
      }
      current_val.model.value = ''
      new_val.model.value = ''
    }
    else {
      const resp: Resp = await accessUserPut(
        param.value, current_val.model.value, new_val.model.value
      )
      if (resp.status === 200) {
        router.push({name: 'user-info'})
      }
      else {
        alert.value = {
          show: true,
          msg: resp.json.msg
        }
        current_val.model.value = ''
        new_val.model.value = ''
      }
    }
  }

  const inputs: Input[] = [
    current_val, new_val
  ]
  const submit: Submit = {
    name: ref('update'), func: (e: MouseEvent) => {tryUpdateUser()}
  }

  onBeforeMount(() => {
    if (GoodParams.includes(param.value)) {
      document.title = 'update ' + param.value
      if (param.value === 'password') {
        current_val.type.value = 'password'
        new_val.type.value = 'password'
      }
    }
    else {
      router.push('/404')
    }
  })
</script>

<template>
  <div class="p-3">
    <AlertBox/>
    <h4 class="fw-bolder mb-3">
      update {{ param }}
    </h4>
    <Form v-bind:inputs="inputs" v-bind:submit="submit"/>
  </div>
</template>

<script setup lang="ts">
  const router = useRouter()
  const route = useRoute()
  const alert = useAlertStore()

  const GoodParams: string[] = [
    'email', 'password', 'name'
  ]

  let param: Ref<string> = ref(route.params.param as string ?? '')
  let type: Ref<string> = ref('password')

  let current_val: Ref<string> = ref('')
  let new_val: Ref<string> = ref('')

  async function tryUpdateUser(): Promise<void> {
    if (current_val.value === '' || new_val.value === '') {
      alert.value = {
        show: true,
        msg: 'Fill all input fields'
      }
      current_val.value = ''
      new_val.value = ''
    }
    else {
      const resp: Resp = await accessUserPut(
        param.value, current_val.value, new_val.value
      )
      if (resp.status === 200) {
        router.push({name: 'user-info'})
      }
      else {
        alert.value = {
          show: true,
          msg: resp.json.msg
        }
        current_val.value = ''
        new_val.value = ''
      }
    }
  }

  onBeforeMount(() => {
    if (GoodParams.includes(param.value)) {
      document.title = 'update ' + param.value
      if (param.value !== 'password') {
        type.value = 'text'
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
    <div class="col-sm-9 col-md-7 col-lg-5 border border-primary bg-light p-3">
      <div class="mb-4">
        <label class="mb-2">current {{ param }}</label>
        <input v-bind:type="type" class="form-control border border-primary" v-model="current_val"/>
      </div>
      <div class="mb-4">
        <label class="mb-2">new {{ param }}</label>
        <input v-bind:type="type" class="form-control border border-primary" v-model="new_val"/>
      </div>
      <br>
      <div>
        <button class="btn btn-primary" v-on:click="tryUpdateUser">update</button>
      </div>
    </div>
  </div>
</template>

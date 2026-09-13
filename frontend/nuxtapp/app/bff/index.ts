import {Hono} from 'hono'
import {bffAuthRoute, bffUserRoute} from '~/composables/ApiClient'
import authRouter from '~/bff/auth'
import userRouter from '~/bff/user'

const app = new Hono().basePath('/bff')

app.route(bffAuthRoute, authRouter)
app.route(bffUserRoute, userRouter)

export default defineEventHandler((event) => {
  return app.fetch(toWebRequest(event))
})

import {Hono} from 'hono'
import {bffUrlBase, bffAuthRoute, bffUserRoute} from '~/composables/ApiClient'
import authRouter from '~/bff/auth'
import userRouter from '~/bff/user'

const app = new Hono().basePath(bffUrlBase)

app.route(bffAuthRoute, authRouter)
app.route(bffUserRoute, userRouter)

export default defineEventHandler((event) => {
  return app.fetch(toWebRequest(event))
})

import {Hono} from 'hono'
import auth_router from './auth'
import user_router from './user'

const app = new Hono().basePath('/bff')

app.route('/auth/', auth_router)
app.route('/user/', user_router)

export default defineEventHandler((event) => {
  return app.fetch(toWebRequest(event))
})

import {Hono} from 'hono'
import {bodyLimit} from 'hono/body-limit'
import {bffUrlBase} from '#shared'
import {routers} from '#server/routers'

const app = new Hono()
  .basePath(bffUrlBase)
  .use(
    bodyLimit({
      maxSize: 1024,
      onError: (c) => c.json({msg: 'Request Entity Too Large'}, 413)
    })
  )

for (const each of routers) {
  app.route(each.route, each.router)
}

export default defineEventHandler((event) => {
  return app.fetch(toWebRequest(event))
})

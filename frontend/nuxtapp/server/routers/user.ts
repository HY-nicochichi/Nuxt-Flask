import {Hono} from 'hono'
import {proxyToApi} from '#server/proxy'

const apiUserRoute = '/users'
export const userRouter = new Hono()

userRouter.post('', (c) => proxyToApi(c, apiUserRoute))
userRouter.get('/me', (c) => proxyToApi(c, apiUserRoute + '/me', 'access'))
userRouter.patch('/me', (c) => proxyToApi(c, apiUserRoute + '/me', 'access'))
userRouter.delete('/me', (c) => proxyToApi(c, apiUserRoute + '/me', 'access'))

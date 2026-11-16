import {bffAuthRoute, bffUserRoute} from '#shared'
import {authRouter} from '#server/routers/auth'
import {userRouter} from '#server/routers/user'

export const routers = [
  {route: bffAuthRoute, router: authRouter},
  {route: bffUserRoute, router: userRouter}
]

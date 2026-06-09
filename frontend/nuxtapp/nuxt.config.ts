export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: {enabled: true},
  ssr: false,
  modules: ['@pinia/nuxt'],
  css: ['~/app.scss'],
  serverHandlers: [{
    route: '/bff/**',
    handler: '~/bff/index.ts',
    middleware: false
  }],
  app: {
    head: {
      htmlAttrs: {lang: 'en'},
      meta: [
        {charset: 'utf-8'},
        {'http-equiv': 'X-UA-Compatible', content: 'IE=edge'},
        {name: 'viewport', content: 'width=device-width,initial-scale=1.0'}
      ],
      link: [
        {rel: 'icon', href: '/favicon.ico'}
      ]
    }
  }
})

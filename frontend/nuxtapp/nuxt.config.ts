export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: {enabled: true},
  ssr: false,
  modules: ['@pinia/nuxt'],
  runtimeConfig: {
    public: {apiUrlBase: process.env.API_URL_BASE}
  },
  app: {
    head: {
      htmlAttrs: {lang: 'en'},
      meta: [
        {charset: 'utf-8'},
        {'http-equiv': 'X-UA-Compatible', content: 'IE=edge'},
        {name: 'viewport', content: 'width=device-width,initial-scale=1.0'}
      ],
      link: [
        {rel: 'icon', href: '/favicon.ico'},
        {
          rel: 'stylesheet',
          href: 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
          integrity: 'sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM',
          crossorigin: 'anonymous'
        }
      ],
      script: [
        {
          src: 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
          integrity: 'sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz',
          crossorigin: 'anonymous',
          defer: true
        }
      ]
    }
  }
})

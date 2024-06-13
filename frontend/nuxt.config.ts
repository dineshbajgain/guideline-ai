// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@pinia/nuxt','nuxt-primevue'],
  plugins: [
    '~/plugins/axios.js'
  ],
  primevue: {

  },
  css: ['primevue/resources/themes/aura-light-green/theme.css']
})

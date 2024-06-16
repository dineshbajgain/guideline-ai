// https://nuxt.com/docs/api/configuration/nuxt-config
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    'nuxt-proxy',
    '@pinia/nuxt',
    (_options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig', (config) => {
        // @ts-expect-error
        config.plugins.push(vuetify({ autoImport: true }))
      })
    },
  ],
  plugins: [
    '~/plugins/axios.js',
    '~/plugins/vuetify.js'
  ],
  build: {
    transpile: ['vuetify'],
  },
  vite: {
    vue: {
      template: {
        transformAssetUrls,
      },
    },
  },
  runtimeConfig:{
    proxy: {
      options: {
        target: process.env.API_BASE_URL || "http://127.0.0.1:5000",
        changeOrigin: true,
        pathRewrite: {
          '^/api': '',
        },
        pathFilter: [
         '/api/clone_rep',
         '/api/get_repo_details',
         '/api/get_dependencies',
         '/api/get_dependencies_history',
         '/api/commit_history',
         '/api/generate_text',
         '/api/sentiment_analysis'
        ],
      }
    },
  }
})

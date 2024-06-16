// plugins/axios.js
import axios from 'axios'

export default defineNuxtPlugin((nuxtApp) => {
  const axiosInstance = axios.create({
    baseURL: '/'
    // You can add other axios configuration here
  })

  // You can also add axios interceptors here
  axiosInstance.interceptors.request.use((config) => {
    // Do something before the request is sent
    return config
  }, (error) => {
    // Do something with request error
    return Promise.reject(error)
  })

  // Adding the axios instance to the Nuxt app
  nuxtApp.provide('axios', axiosInstance)
})

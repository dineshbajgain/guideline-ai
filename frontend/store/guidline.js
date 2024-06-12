import { defineStore } from 'pinia'
export const useGuidlineStore = defineStore('guidline', {
  state: () => ({
    url: '',
    learningPath:[]
  }),
  actions: {
    resetUrl(){
        this.url = '';
        this.learningPath = []
    }, 
    updateUrl(url){
        this.url = url
        this.createLearningPath({repo_url: url})
    },
    // createLearningPath
    async createLearningPath(path){
        const { $axios } = useNuxtApp()
        try {
            const response = await $axios.post('/createLearningPath', path)
            this.learningPath = response.data
        } catch (error) {
            console.error(error)
        }
    },
  }
})

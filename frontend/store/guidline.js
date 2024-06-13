import { defineStore } from 'pinia'
export const useGuidlineStore = defineStore('guidline', {
  state: () => ({
    url: '',
    learningPath:[],
    totalDependencies: 0,
    analyzeData: {}
  }),
  actions: {
    resetUrl(){
        this.url = '';
        this.learningPath = [];
        this.totalDependencies= 0;
        this.analyzeData = {};
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
            this.totalDependencies= response.data.length
        } catch (error) {
            console.error(error)
        }
    },
    async getRepoAnalysis(){
        const { $axios } = useNuxtApp()
        try {
            const response = await $axios.post('/getRepoAnalysis',{repo_url: this.url})
            this.analyzeData =  response.data
        } catch (error) {
            console.error(error)
        }
    }
  }
})

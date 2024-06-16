import { defineStore } from 'pinia'

export const guidlineStore = defineStore('guidline', {
  state: () => ({
    url: '',
    learningPath:[],
    totalDependencies: 0,
    allDependencies: [],
    dependencyHistory: [],
    repoDetails: {},
    commitHistory: [],
    sentimentAnalysisData: {},
    loading: false,
    generatedText: '',
    cloneMessage: '',
  }),
  actions: {
    resetUrl(){
        this.url= '';
        this.learningPath=[];
        this.totalDependencies= 0;
        this.allDependencies= [];
        this.dependencyHistory= [];
        this.repoDetails= {};
        this.commitHistory= [];
        this.sentimentAnalysisData= {};
        this.loading= false;
        this.generatedText= '';
    }, 
    updateUrl(url){
        this.url = url
    },
    setLoading(loading){
        this.loading = loading
    },
    // cloneRepo
    async postCloneRepo(){
        const { $axios } = useNuxtApp()
        try {
            const response = await $axios.post('/api/clone_repo', {repo_url: this.url})
            return response.data
        } catch (error) {
            console.error(error)
        }
    },
    // getRepoDetails
    async postGetRepoDetails(){
        const { $axios } = useNuxtApp()
        try {
            const response = await $axios.post('/api/get_repo_details', {
                repo_url: this.url,
                custom_day: 30
            })
            this.repoDetails = response.data
        } catch (error) {
            console.error(error)
        }
    },
    // getDependencies
    async postGetDependencies(){
        const { $axios } = useNuxtApp()
        try {
            const response = await $axios.post('/api/get_dependencies', {repo_url: this.url})
            this.allDependencies = response.data
            this.totalDependencies= response.data.length
        } catch (error) {
            console.error(error)
        }
    },
    // getDependenciesHistory
    async postGetDependenciesHistory(dependency){
        const { $axios } = useNuxtApp()
        try {
            const response = await $axios.post('/api/get_dependencies_history', {
                repo_url: this.url,
                package_name: dependency
            })
            this.dependencyHistory = response.data
        } catch (error) {
            console.error(error)
        }
    },
    // commit_history
    async postGetCommitHistory(){
        const { $axios } = useNuxtApp()
        try {
            const response = await $axios.post('/api/commit_history', {repo_url: this.url})
            this.commitHistory = response.data
        } catch (error) {
            console.error(error)
        }
    },
    // generateText
    async postGetGenerateText(dependency){
        const { $axios } = useNuxtApp()
        try {
            const response = await $axios.post('/api/generate_text', {dependency: dependency})
            this.generatedText = response.data
        } catch (error) {
            console.error(error)
        }
    },
    // sentimentAnalysis
    async postGetUserSentimentAnalysis(){
        const { $axios } = useNuxtApp()
        try {
            const response = await $axios.post('/api/sentiment_analysis', {repo_url: this.url})
            this.sentimentAnalysisData = response.data
        } catch (error) {
            console.error(error)
        }
    },
  }
})

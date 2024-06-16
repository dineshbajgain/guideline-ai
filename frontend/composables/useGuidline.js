import { guidlineStore } from '../store/guidline.js'
import { storeToRefs } from 'pinia'
export const useGuidline = () => {
  const { loading, repoDetails, allDependencies, dependencyHistory, sentimentAnalysisData, commitHistory } = storeToRefs(guidlineStore())
    const nuxtApp = useNuxtApp()
    const store = guidlineStore()
    const isLoading = computed(() => store.loading)
    const githubUrl = computed(() => store.url)
    const updateUrl = (url) => store.updateUrl(url)
    const setLoading = (loading) => store.setLoading(loading)
    const setAllDependencies = (changeProgress) =>{
      debugger
       store.setAllDependencies(changeProgress)}
    const cloneRepo = () => store.postCloneRepo()
    const getRepoDetails = () => store.postGetRepoDetails()
    const getDependencies = () => store.postGetDependencies()
    const getDependenciesHistory = (dependency) => store.postGetDependenciesHistory(dependency)
    const getCommitHistory = () => store.postGetCommitHistory()
    const postGetGenerateText = (dependency) => store.postGetGenerateText(dependency)
    const postGetUserSentimentAnalysis = (user_name) => store.postGetUserSentimentAnalysis(user_name)
    const squadConfidence = computed(() => {
      let sum = 0
      allDependencies.value.forEach((dependency) => {
        sum += dependency.progress
      })
      console.log(sum)
      return sum / allDependencies.value.length
    })
    watch(githubUrl, async () => {
      if (store.url) {
       const response = await cloneRepo()
       await getRepoDetails()
       await getDependencies()
       if(response.message === 'Success'){
        setLoading(false)
       }
      }
    })
    return { setAllDependencies, squadConfidence, loading, repoDetails, allDependencies, dependencyHistory, sentimentAnalysisData, commitHistory, updateUrl, setLoading, cloneRepo, getRepoDetails, getDependencies, getDependenciesHistory, getCommitHistory, postGetGenerateText, postGetUserSentimentAnalysis }
  }
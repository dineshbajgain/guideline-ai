import { guidlineStore } from '../store/guidline.js'
import { storeToRefs } from 'pinia'
export const useGuidline = () => {
  const { loading, repoDetails, allDependencies,dependencyHistory } = storeToRefs(guidlineStore())
    const nuxtApp = useNuxtApp()
    const store = guidlineStore()
    const isLoading = computed(() => store.loading)
    const githubUrl = computed(() => store.url)
    const updateUrl = (url) => store.updateUrl(url)
    const setLoading = (loading) => store.setLoading(loading)
    const cloneRepo = () => store.postCloneRepo()
    const getRepoDetails = () => store.postGetRepoDetails()
    const getDependencies = () => store.postGetDependencies()
    const getDependenciesHistory = (dependency) => store.postGetDependenciesHistory(dependency)
    const getCommitHistory = () => store.postGetCommitHistory()
    const postGetGenerateText = (dependency) => store.postGetGenerateText(dependency)
    const postGetUserSentimentAnalysis = () => store.postGetUserSentimentAnalysis()
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
    return { loading, repoDetails, allDependencies, dependencyHistory, updateUrl, setLoading, cloneRepo, getRepoDetails, getDependencies, getDependenciesHistory, getCommitHistory, postGetGenerateText, postGetUserSentimentAnalysis }
  }
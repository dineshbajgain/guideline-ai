<template>
    <div class="markdown-body" v-html="readmeContent"></div>
</template>
  
<script setup>
import { marked } from 'marked';
import { computed } from 'vue';
  const props = defineProps({
    readme: String
})
const readmeContent = computed(()=> marked(props.readme || ""))
</script>
  
<style>
  @import 'github-markdown-css/github-markdown.css';
  
  .markdown-body {
    box-sizing: border-box;
    min-width: 200px;
    max-width: 980px;
    margin: 0 auto;
    padding: 45px;
  }
</style>
  
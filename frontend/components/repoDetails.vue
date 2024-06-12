<template>
    <div class="repo-card">
        <div class="repo-card-header">
            <h2>{{ repo.name }}</h2>
            <p>{{ repo.description }}</p>
        </div>
        <div class="repo-card-body">
            <div class="repo-card-body-left">
                <p>Stars: {{ repo.stargazers_count }}</p>
                <p>Issues: {{ repo.open_issues_count }}</p>
            </div>
            <div class="repo-card-body-right">
                <p>Language: {{ repo.language }}</p>
                <p>License: {{ repo.license?.name }}</p>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue'
const repo = ref({
    name: 'vue',
    description: 'Vue.js is a progressive framework for building user interfaces.',
    stargazers_count: 100000,
    open_issues_count: 1000,
})
</script>
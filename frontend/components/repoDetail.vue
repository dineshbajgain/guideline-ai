<template>
    <v-card class="mx-auto">
        <template v-slot:title>
            <span class="font-weight-black">Details of Repo [{{ repoDetails.repo_name }}]</span>
        </template>
        <v-card-text class="bg-surface-light pt-4">
            <div class="d-flex">
                <div class="repo-data-row">
                    <div class="individual-data">
                        Repo Name :{{ repoDetails.repo_name }}
                    </div>
                    <div class="individual-data">
                        Language :{{ repoDetails.language }}
                    </div>
                    <div class="individual-data">
                        Default Branch :{{ repoDetails.default_branch }}
                    </div>
                    <div class="individual-data">
                        Total Commits :{{ repoDetails.total_commits }}
                    </div>
                    <div class="individual-data">
                        Total Prs :{{ repoDetails.total_prs }}
                    </div>
                </div>
                <div class="repo-data-row">
                    <div class="individual-data">
                        Total Branches :{{ repoDetails.total_branches }}
                    </div>
                    <div class="individual-data">
                        Total Contributors :{{ repoDetails.total_contributors - 1 }} + Contributers
                    </div>
                    <!-- <div class="individual-data">
                        contributors :
                        <template v-for="contributor in analyzeData.contributors" >
                            <Button type="button" :label="contributor.name" icon="pi pi-inbox" :badge="contributor.contribution" badgeSeverity="contrast" outlined />
                        </template>
                    </div> -->
                    <div class="individual-data">
                        Last Update : {{ repoDetails.last_update }}
                    </div>
                    <div class="individual-data">
                        Reviewer :
                        <v-btn
                        class="ma-2"
                    prepend-icon="mdi-account-circle"
                    v-for="reviewer in repoDetails.reviewers" :key="reviewer"
                    >
                    <template v-slot:prepend>
                        <v-icon color="success"></v-icon>
                    </template>
                    {{ reviewer }}
                    </v-btn>
                    </div>
                </div>
            </div>
        </v-card-text>
    </v-card>
</template>

<script setup>
const { repoDetails } = useGuidline()

// import { useGuidlineStore } from '~/store/guidline.js'
// const guidlineStore = useGuidlineStore();
// const analyzeData = ref({});
// guidlineStore.getRepoAnalysis();
// watch(() => guidlineStore.analyzeData, (newVal, oldVal) => {
//     analyzeData.value = guidlineStore.analyzeData;
// });
</script>
<style scoped>
.flex {
    display: flex;
}

.individual-data {
    font-size: 18px;
    line-height: 40px;
}

.repo-data-row {
    padding: 20px 150px 20px 0px;
}
</style>
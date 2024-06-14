<template>
    <v-card class="mx-auto">
        <template v-slot:title>
            <span class="font-weight-black">Details of Repo [{{ analyzeData.repo_name }}]</span>
        </template>
        <v-card-text class="bg-surface-light pt-4">
            <div class="d-flex">
                <div class="repo-data-row">
                    <div class="individual-data">
                        Repo Name :{{ analyzeData.repo_name }}
                    </div>
                    <div class="individual-data">
                        Language :{{ analyzeData.language }}
                    </div>
                    <div class="individual-data">
                        Default Branch :{{ analyzeData.default_branch }}
                    </div>
                    <div class="individual-data">
                        Total Commits :{{ analyzeData.total_commits }}
                    </div>
                    <div class="individual-data">
                        Total Prs :{{ analyzeData.total_prs }}
                    </div>
                </div>
                <div class="repo-data-row">
                    <div class="individual-data">
                        Total Branches :{{ analyzeData.total_branches }}
                    </div>
                    <div class="individual-data">
                        Total Contributors :{{ analyzeData.total_contributors - 1 }} + Contributers
                    </div>
                    <!-- <div class="individual-data">
                        contributors :
                        <template v-for="contributor in analyzeData.contributors" >
                            <Button type="button" :label="contributor.name" icon="pi pi-inbox" :badge="contributor.contribution" badgeSeverity="contrast" outlined />
                        </template>
                    </div> -->
                    <div class="individual-data">
                        Last Update : {{ analyzeData.last_update }}
                    </div>
                </div>
            </div>
        </v-card-text>
    </v-card>
</template>

<script setup>
import { useGuidlineStore } from '~/store/guidline.js'
const guidlineStore = useGuidlineStore();
const analyzeData = ref({});
guidlineStore.getRepoAnalysis();
watch(() => guidlineStore.analyzeData, (newVal, oldVal) => {
    analyzeData.value = guidlineStore.analyzeData;
});
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
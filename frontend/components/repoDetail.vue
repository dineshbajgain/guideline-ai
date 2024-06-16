<template>
    <div>
    <v-card class="mx-auto">
        <template v-slot:title>
            <div class="d-flex">
                <span class="font-weight-black">Details of Repo [{{ repoDetails.repo_name }}]</span>
                <div class="ml-auto w-custom">
                    <v-select density="compact" variant="outlined" :items="items" v-model="selectedSquad" item-title="name" label="Squad">
                        <template v-slot:item="{ props, item }">
                        <v-list-item v-bind="props" :subtitle="item.raw.department"></v-list-item>
                        </template>
                    </v-select>
                </div>
            </div>
        </template>
        <v-card-text class="bg-surface-light pt-4">
            <div class="d-flex">
                <div class="repo-data-row">
                    <div class="individual-data">
                        Repo Name :{{ repoDetails.repo_name }}
                    </div>
                    <div class="individual-data">
                        Language :{{ repoDetails.language || "Java Script" }}
                    </div>
                    <div class="individual-data">
                        Default Branch :{{ repoDetails.default_branch }}
                    </div>
                    <div class="individual-data">
                        Total Commits :{{ repoDetails.total_commits }}
                        <v-btn
                            class="ma-2"
                            color="purple"
                            icon="mdi-history"
                            size="small"
                            variant="text"
                            @click="openCommitHistory"
                        ></v-btn>
                    </div>
                    <div class="individual-data">
                        Total Prs :{{ repoDetails.total_prs || "***" }}
                    </div>
                </div>
                <div class="repo-data-row">
                    <div class="individual-data">
                        Total Branches :{{ repoDetails.total_branches }}
                    </div>
                    <div class="individual-data">
                        Total Contributors :{{ repoDetails.total_contributors - 1 }} + Contributers
                        <v-btn v-if="selectedSquad" @click="dialog = true" small>Squad contributers</v-btn>
                    </div>
                    <div v-if="selectedSquad" class="individual-data">
                        Squad Confidence : <v-chip color="primary" variant="flat">
                            {{ squadConfidence.toFixed(2) }} %
                    </v-chip>
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
    <v-dialog
      v-model="dialog"
      width="600"
    >
      <v-card
        max-width="600"
        title="Squad Members"
      >
       <template v-slot:default>
        <div class="d-flex">
            <v-btn
            @click="openSheet(member)"
                            class="ma-2"
                        prepend-icon="mdi-account-circle"
                        v-for="member in squadMember" :key="member"
                        >
                        <template v-slot:prepend>
                            <v-icon color="success"></v-icon>
                        </template>
                        {{ member }}
            </v-btn>
                    </div>
        </template>
        <template v-slot:actions>
          <v-btn
            class="ms-auto"
            text="Ok"
            @click="dialog = false"
          ></v-btn>
        </template>
      </v-card>
    </v-dialog>
    <v-bottom-sheet v-if="sentimentAnalysisData && sheet" v-model="sheet">
      <v-card
        class="text-center"
        height="400"
      >
        <v-card-text>
          <v-btn
            variant="text"
            @click="sheet = !sheet"
          >
            close
          </v-btn>

          <br>
          <br>
            <div class="d-flex flex-column">
                <v-slider
                v-model="sliderValue"
                :color="sheetData.color"
                thumb-label="always"
            >
                <template v-slot:thumb-label="{  }">
                    {{ satisfactionEmojis[sheetData.index] }}
                </template>
                </v-slider>
                <template v-if="loading">
                    <v-skeleton-loader
                        class="my-10"
                        elevation="4"
                        type="paragraph"
                        boilerplate
                    ></v-skeleton-loader>
                </template>
                <template v-else>
                    <div>
                    <span>Stress Level: {{ sheetData.pressure }}</span>
                </div>
                <div>
                    <span>Recommendations: </span>
                    <template v-if="sheetData.compliments.length > 0">
                        <v-alert
                            v-for="(compliment, index) in sheetData.compliments"
                            :key="index"
                            :text="compliment"
                            type="success"
                            class="ma-2"
                        ></v-alert>
                    </template>
                </div>
                    </template>
            </div>
        </v-card-text>
      </v-card>
    </v-bottom-sheet>
    <v-navigation-drawer
                    v-if="drawer"
                    v-model="drawer"
                    temporary
                    location="right"
                    :width="600"
                    theme="light"

                >
                    <v-card>
                        <v-card-title>
                            Commit History Last 30 days
                        </v-card-title>
                        <v-card-text></v-card-text>
                            <v-list>
                                <v-list-item
                                    v-for="commit in commitHistory"
                                    :key="commit.commit_id"
                                >
                                <v-card variant="outlined" class="pa-2">
                            
                                    <v-list-item-subtitle>
                                        User Name: {{ commit.username}}
                                    </v-list-item-subtitle>
                                    <v-list-item-subtitle>
                                       Last Commit : {{ commit.diff_days }} Days Ago
                                    </v-list-item-subtitle>
                                    <v-list-item-subtitle>
                                        Commit Message : {{ commit.commit_message }} Days Ago
                                    </v-list-item-subtitle>
                                    <v-list-item-subtitle>
                                        Commit Id: {{ commit.commit_id }} Days Ago
                                    </v-list-item-subtitle>
                                </v-card>
                            </v-list-item>

                            </v-list>
                    </v-card>
    </v-navigation-drawer>
    </div>
</template>

<script setup>

const { loading, repoDetails, postGetUserSentimentAnalysis, sentimentAnalysisData,getCommitHistory, commitHistory, setLoading, squadConfidence } = useGuidline()
const items = [
    {
        name: 'dhaulagiri',
        department: 'dhaulagiri'
    },
]
const squadMember = [
    'dinesh bajgain',
    'sanishUBA',
    'amirshrestha',
]
const selectedSquad = ref(null)
const dialog = ref(false)
const sheet = ref(false)
const drawer = ref(false)
const slider = ref([
    {
        index: 0,
        pressure:"Low",
        value: 10,
        color: "green",
        compliments:[]
    },
    {
        index: 1,
        pressure:"Medium",
        value: 50,
        color: "yellow",
        compliments:[]
    },
    {
        index: 2,
        pressure:"High",
        value: 100,
        color: "red",
        compliments:[]
    },
])
const sheetData = ref({
    index: 0,
    pressure:"Low",
    value: 10,
    color: "green",
    compliments:[]
})
const openSheet = async (member) => {
    setLoading(true)
    sheet.value = !sheet.value
    const sentimentResponse  = await postGetUserSentimentAnalysis(member)
    if(sentimentResponse.error){
        sheetData.value = slider.value.find((item) => item.pressure == 'Low')
        sheetData.value.compliments = [sentimentResponse.error]
    }else{
        sheetData.value = slider.value.find((item) => item.pressure == sentimentAnalysisData.value.stress_level)
        sheetData.value.compliments = sentimentAnalysisData.value.recommendations
    }
    setLoading(false)
}
const openCommitHistory = () => {
    drawer.value = true
    getCommitHistory()
}
const sliderValue = computed(()=>sheetData.value.value || 10)
const satisfactionEmojis = ['😍', '😊', '😡']
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
.w-custom {
    width: 20%;
}
</style>
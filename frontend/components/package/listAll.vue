
<template>
    <div>
        <div>
            <repoDetail :class="{'repo-content mx-4': true, 'top': isTop, 'center': !isTop}" />
        </div>
            <v-timeline align="start">
                <v-timeline-item
                    v-for="(item, i) in allDependencies"
                    :key="i"
                    :dot-color="colors[Math.floor(Math.random()*colors.length)]"
                    :icon="icons[Math.floor(Math.random()*icons.length)]"
                    fill-dot
                >
                    <v-card class="mx-4">
                    <v-card-title @click="dependencyDetails(item)" :class="['text-h6', `bg-${colors[Math.floor(Math.random()*colors.length)]}`]">
                        {{ item.dependency }}
                    </v-card-title>
                    
                    </v-card>
                </v-timeline-item>
            </v-timeline>
            <v-navigation-drawer
                    v-if="drawer"
                    v-model="drawer"
                    temporary
                    location="right"
                    :width="600"
                >
                <template v-if="loading">
                    <v-skeleton-loader
                        v-for="i in 5"
                        :key="i"
                        class="my-10"
                        elevation="4"
                        type="paragraph"
                        boilerplate
                    ></v-skeleton-loader>
                </template>
                    <v-card v-else> 
                        <v-card-title>
                            <div class="d-flex justify-space-between">
                                <div>
                                    {{ drawerData.dependency }}
                                </div>
                                <v-select
                                    label="Select"
                                    :items="packageKnowledgeStatus"
                                    v-model="progress"
                                    item-title="title"
                                    item-value="value"
                                    variant="outlined"
                                    density="compact"
                                    max-width="200"
                                    ></v-select>
                            </div>
                        </v-card-title>
                        <v-card-text v-if="dependencyHistory.readme">
                            <v-card>
                                <v-card-text>
                                    <v-table>
                                        <tr>
                                            <td>Added By</td>
                                            <td>{{ dependencyHistory.added_by.username }}</td>
                                        </tr>
                                        <tr>
                                            <td>Added On</td>
                                            <td>{{ dependencyHistory.added_by.date_time }}</td>
                                        </tr>
                                        <tr>
                                            <td>Github URL</td>
                                            <td>{{ dependencyHistory.github_url }}</td>
                                        </tr>
                                        <tr>
                                            <td>Npm URL</td>
                                            <td>{{ dependencyHistory.npm_url }}</td>
                                        </tr>
                                        <tr>
                                            <td>version</td>
                                            <td>{{ dependencyHistory.version }}</td>
                                        </tr>
                                    </v-table>
                                </v-card-text>
                            </v-card>
                            <readmeDisplay :readme="dependencyHistory.readme" />
                            <!-- {{ dependencyHistory.readme }} -->
                            <!-- <VueMarkdown :source="dependencyHistory.readme" /> -->
                        </v-card-text>
                        </v-card>
                </v-navigation-drawer>
    </div>
</template>

<script setup>
import repoDetail from '~/components/repoDetail.vue'
import readmeDisplay from '~/components/readmeDisplay.vue'
import { watch } from 'vue'
const { loading, allDependencies, getDependenciesHistory, dependencyHistory, setLoading, setAllDependencies } = useGuidline()
const isTop = ref(true)
const drawer = ref(false)
const drawerData = ref(null);

const dependencyDetails = async (item) => {
    setLoading(true);
    drawer.value = true;
    drawerData.value = item;
    await getDependenciesHistory(item.dependency)
    progress.value = packageKnowledgeStatus.value.find((status) => status.value == item.progress);
    setLoading(false);
}
const colors =['red-lighten-2','purple-lighten-2','green-lighten-1','indigo-lighten-2'];
const icons = ['mdi-star','mdi-book-variant','mdi-airballoon','mdi-layers-triple'];
const progress = ref({
    title: 'Not Known',
    value: '0'
});
const packageKnowledgeStatus = ref([
{
    title: 'Not Known',
    value: '0'
},
{
    title: 'Known',
    value: '30'
},{
    title: 'Learning',
    value: '70'
},{
    title: 'Expert',
    value: '100'
}
])
watch(progress, (newVal) => {
    setAllDependencies({
        dependency: drawerData.value.dependency,
        progress: parseInt(newVal.value || newVal)
    })
})
</script>

<style lang="scss" scoped>
@media screen and (max-width: 960px) {
    ::v-deep(.customized-timeline) {
        .p-timeline-event:nth-child(even) {
            flex-direction: row;

            .p-timeline-event-content {
                text-align: left;
            }
        }

        .p-timeline-event-opposite {
            flex: 0;
        }
    }
}
.repo-details{
    padding: 2em 1em;
}
</style>

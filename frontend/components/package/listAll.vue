
<template>
    <div>
        <div>
            <repoDetail :class="{'repo-content': true, 'top': isTop, 'center': !isTop}" />
        </div>
            <v-timeline align="start">
                <v-timeline-item
                    v-for="(item, i) in allDependencies"
                    :key="i"
                    :dot-color="colors[Math.floor(Math.random()*colors.length)]"
                    :icon="icons[Math.floor(Math.random()*icons.length)]"
                    fill-dot
                >
                    <v-card>
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
                    <v-card>
                        <v-card-title>
                            {{ drawerData.dependency }}
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
const { loading, allDependencies, getDependenciesHistory, dependencyHistory } = useGuidline()
const isTop = ref(true)
const drawer = ref(false)
const drawerData = ref(null);

const dependencyDetails = (item) => {
    drawer.value = true;
    drawerData.value = item;
    getDependenciesHistory(item.dependency)
}
// const guidlineStore = useGuidlineStore()
// const events = ref(guidlineStore.learningPath);
// const generatedText = ref('');
// const visible = ref(false);
// const changeVisible = () => {
//     visible.value = !visible.value;
// }
// //

const colors =['red-lighten-2','purple-lighten-2','green-lighten-1','indigo-lighten-2'];
const icons = ['mdi-star','mdi-book-variant','mdi-airballoon','mdi-layers-triple'];
// const drawer = ref(false);
// const drawerData = ref(null);
// const checkData = (item) => {
//     drawer.value = true;
//     guidlineStore.generateText(item.dependency)
//     drawerData.value = item;
// }
// watch(() => guidlineStore.generatedText, (value) => {
//     generatedText.value = value.resources.join(' ');
// })
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

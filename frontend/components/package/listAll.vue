
<template>
    <div>
        <div>
            <repoDetails :class="{'repo-content': true, 'top': isTop, 'center': !isTop}" />
        </div>
            <v-timeline align="start">
                <v-timeline-item
                    v-for="(item, i) in events"
                    :key="i"
                    :dot-color="colors[Math.floor(Math.random()*colors.length)]"
                    :icon="icons[Math.floor(Math.random()*icons.length)]"
                    fill-dot
                >
                    <v-card>
                    <v-card-title @click="checkData(item)" :class="['text-h6', `bg-${colors[Math.floor(Math.random()*colors.length)]}`]">
                        {{ item.dependency }}
                    </v-card-title>
                    
                    </v-card>
                </v-timeline-item>
                <v-navigation-drawer
                    v-model="drawer"
                    temporary
                    location="right"
                    :width="400"
                >
                <v-card>
                    <v-card-title>
                        {{ drawerData.dependency }}
                    </v-card-title>
                    <v-card-text>
                        <VueMarkdown :source="generatedText" />
                    </v-card-text>
                    </v-card>
                </v-navigation-drawer>
            </v-timeline>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { useGuidlineStore } from '~/store/guidline.js'
import repoDetails from '~/components/repoDetails.vue'
import VueMarkdown from 'vue-markdown-render'

const guidlineStore = useGuidlineStore()
const events = ref(guidlineStore.learningPath);
const generatedText = ref('');
const visible = ref(false);
const changeVisible = () => {
    visible.value = !visible.value;
}
//

const colors =['red-lighten-2','purple-lighten-2','green-lighten-1','indigo-lighten-2'];
const icons = ['mdi-star','mdi-book-variant','mdi-airballoon','mdi-layers-triple'];
const drawer = ref(false);
const drawerData = ref(null);
const checkData = (item) => {
    drawer.value = true;
    guidlineStore.generateText(item.dependency)
    drawerData.value = item;
}
watch(() => guidlineStore.generatedText, (value) => {
    generatedText.value = value.resources.join(' ');
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

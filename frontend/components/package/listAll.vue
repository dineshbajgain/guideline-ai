
<template>
    <div class="card">
        <transition-group name="list">
          
        <Timeline :value="events" align="alternate" class="customized-timeline">
            <template #marker="slotProps">
                <span class="flex w-2rem h-2rem align-items-center justify-content-center text-white border-circle z-1 shadow-1" :style="{ backgroundColor: slotProps.item.color }">
                    <i :class="slotProps.item.icon"></i>
                </span>
            </template>
            <template #content="slotProps">
                <Card class="mt-3">
                    <template #title>
                        {{ slotProps.item.dependency }}
                    </template>
                    <template #subtitle>
                        {{ slotProps.item.date }}
                    </template>
                    <template #content>
                        
                        <Button label="Read more" text></Button>
                    </template>
                </Card>
            </template>
        </Timeline>
        </transition-group>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { useGuidlineStore } from '~/store/guidline.js'
const guidlineStore = useGuidlineStore()
const events = ref(guidlineStore.learningPath);

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
</style>

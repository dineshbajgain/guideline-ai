
<template>
    <div class="card">
        <div class="flex gap-2 justify-center">
            <Button icon="pi pi-arrow-right" @click="visibleLeft = true" />
            <Button icon="pi pi-arrow-left" @click="visibleRight = true" />
            <Button icon="pi pi-arrow-down" @click="visibleTop = true" />
            <Button icon="pi pi-arrow-up" @click="visibleBottom = true" />
        </div>
        <Drawer :visible="visibleRight" header="Right Drawer" position="right">
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
        </Drawer>
    </div>
</template>

<script setup>
import { ref } from "vue";

const visibleLeft = ref(false);
const visibleRight = ref(false);
const visibleTop = ref(false);
const visibleBottom = ref(false);
</script>

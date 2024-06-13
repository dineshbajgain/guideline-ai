<template>
  <div class="body">
    <div :class="{'input-box': true, 'top': isTop, 'center': !isTop}">
      <input type="text" v-model="url">
      <button v-if="!isTop" @click="updateUrl">Start</button>
      <button v-else @click="resetUrl">Reset</button>
    </div>
    <ProgressSpinner v-if="isLoading" class="spinner" />
    <listAll v-if="totalDependencies > 0" :class="{'list-all': true, 'top': isTop, 'center': !isTop}" />
  </div>
</template>
<script setup>
import 'primevue/resources/themes/aura-light-green/theme.css'
import { useGuidlineStore } from '~/store/guidline.js'
import listAll from '~/components/package/listAll.vue'
const guidlineStore = useGuidlineStore()
const url = ref('')
const isTop = ref(false)
const totalDependencies = ref(guidlineStore.totalDependencies)
const isLoading = ref(false)
watch(() => guidlineStore.totalDependencies, (newVal, oldVal) => {
  totalDependencies.value = guidlineStore.totalDependencies
  isTop.value = totalDependencies.value>0 && true  // Toggle isTop
});

const updateUrl = async () => {
  isLoading.value = true
  await guidlineStore.updateUrl(url.value)
}

const resetUrl = () => {
  url.value = ''
  guidlineStore.resetUrl()
  isTop.value = false  // Toggle isTop
}
</script>
<style scoped>
/* background black with lighting input fuld of 50% width */

.list-all{
  background-image: url('./public/git.webp');
  background-size: contain;
  width: 100%;
}
.body {
  background-color: black;
  background-image: url('./public/git.webp');
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
input {
  font-size: 20px;
  width: 50em;
  padding: 20px;
  border-radius: 5px;
  border: none;
}
button {
  margin-left: 10px;
  padding: 15px;
  border-radius: 5px;
  border: none;
  background-color: #000000;
  color: white;
  font-size: 20px;
  border: 1px solid white;
}
.input-box{
  transition: all 0.5s ease; /* Add this line */
}
.input-box.center {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}
.input-box.top {
  margin-top: 30px;
  position: absolute;
  top: 0;
}
.spinner {
  position: relative;
  margin-top: 10em;
}
.list-all{
  position: relative;
  margin-top: 40em;
  transition: all 0.5s ease; /* Add this line */
}
.list-all.center {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}
.list-all.top {
  margin-top: 7em;
  position: absolute;
  top: 0;
}
</style>

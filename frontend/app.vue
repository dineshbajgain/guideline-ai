<template>
  <div class="body">
    <div :class="{'input-box': true, 'top': isTop, 'center': !isTop}">
      <input type="text" v-model="url">
      <button v-if="!isTop" @click="updateUrl">Start</button>
      <button v-else @click="resetUrl">Reset</button>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useGuidlineStore } from '~/store/guidline.js'
const guidlineStore = useGuidlineStore()
const url = ref('')
const isTop = ref(false)
const updateUrl = () => {
  guidlineStore.updateUrl(url.value)
  isTop.value = true  // Toggle isTop
}
const resetUrl = () => {
  guidlineStore.resetUrl()
  isTop.value = false  // Toggle isTop
}
</script>
<style scoped>
/* background black with lighting input fuld of 50% width */
.body {
  background-color: black;
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
</style>

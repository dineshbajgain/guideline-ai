<template>
    <div>
      <div class="body">
      <div :class="{'input-box': true, 'top': isTop, 'center': !isTop}">
        <div class="d-flex">
            <v-text-field
        v-model="url"
        color="primary"
        label="Enter Your Github URL"
        variant="outlined"
      ></v-text-field>
      <div class="mx-4">
        <v-btn variant="outlined" size="x-large" v-if="!isTop" @click="updateGitUrl">Start</v-btn>
        <v-btn v-else variant="outlined" size="x-large"  @click="reset">Reset</v-btn>
      </div>
      </div>
        </div>
        <v-progress-circular
          color="primary"
          v-if="loading"
          indeterminate
        ></v-progress-circular>
    </div>
    <div class="main-body">
      <div class="flex">
        <listAll v-if="allDependencies.length > 0" :class="{'list-all': true, 'top': isTop, 'center': !isTop}" />
      </div>
    </div>
    </div>
</template>
<script setup>
  import listAll from '@/components/package/listAll.vue'
  const { updateUrl, loading, setLoading, allDependencies, resetStore } = useGuidline()
  const isTop = ref(false)
  const url = ref('')
  const updateGitUrl =()=>{
    setLoading(true)
    updateUrl(url.value)
    isTop.value = true
  }
  const reset =()=>{
    url.value = ''
    resetStore()
    isTop.value = false
  }
</script>
<style scoped>
  /* background black with lighting input fuld of 50% width */
  
  .list-all{
    width: 100%;
  }
  .body {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-image: url('../public/git.webp');
    background-size: cover;
  }
  input {
    font-size: 20px;
    width: 50em;
    padding: 20px;
    border-radius: 5px;
    border: none;
  }
  .input-box{
    width: 80%;
    transition: all 0.5s ease; /* Add this line */
  }
  .input-box.center {
    position: absolute;
    top: 45%;
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
  .repo-details,.list-all{
    position: relative;
    margin-top: 40em;
    transition: all 0.5s ease; /* Add this line */
  }
  .repo-details.center,.list-all.center {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
  }
  .repo-details.top,.list-all.top {
    margin-top: 7em;
    position: absolute;
    top: 0;
  }
  .main-body{
    z-index: 1;
    margin-top: 10em;
  }
  </style>
  
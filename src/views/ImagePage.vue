<template>
  <div id="app">
    <p>Still working on this page......</p>
    <button class="btn" @click="goBack">Back to Home</button>
  </div>
</template>

<script>
export default {
  methods: {
    goBack() {
      this.$router.push('/')
    },
  },
}
</script>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  font-family: Arial, sans-serif;
}

.btn {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #009688;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn:hover {
  background-color: #00695c;
}
</style>
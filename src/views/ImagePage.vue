<template>
  <div>
    <p>Still working on this page......</p>
    <button @click="goBack">Back to Home</button>
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

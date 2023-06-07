<template>
  <div id="drag-drop-area">
    <input type="file" id="file" @change="previewImage" ref="fileUpload" style="display: none" />
    <div id="drop-area" @drop="dropHandler" @dragover.prevent>
      <p>Drug and drop your file here</p>
      <button @click="triggerFileUpload">Choose File</button>
    </div>
    <img id="preview" :src="image" v-if="image" />
    <button @click="goToImagePage">Image Library</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      image: null,
    }
  },
  methods: {
    triggerFileUpload() {
      this.$refs.fileUpload.click()
    },
    dropHandler(e) {
  const file = e.dataTransfer.files[0]
  if (file) {
    this.createImage(file)
  }
},
previewImage(e) {
  const file = e.target.files[0]
  if (file) {
    this.createImage(file)
  }
},
createImage(file) {
  const reader = new FileReader()
  reader.onload = (e) => {
    this.image = e.target.result
  }
  reader.readAsDataURL(file)
},

    goToImagePage() {
      this.$router.push('/image')
    },
  },
}
</script>

<style scoped>
/* ... */
</style>

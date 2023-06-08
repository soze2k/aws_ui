<template>
  <div id="app">
    <div id="drag-drop-area">
      <input type="file" id="file" @change="previewImage" ref="fileUpload" style="display: none" />
      <div id="drop-area" @drop="dropHandler" @dragover.prevent>
        <p>Drug and drop your file here</p>
        <button @click="triggerFileUpload">Choose File</button>
      </div>
      <div id="image-preview">
        <img id="preview" :src="image" v-if="image" />
      </div>
      <button class="btn" @click="goToImagePage">Image Library</button>
    </div>
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
#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  font-family: Arial, sans-serif;
}

#drag-drop-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 2px dashed #aaa;
  border-radius: 5px;
}

#drop-area p {
  margin-bottom: 10px;
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

#image-preview {
  max-width: 500px;
  margin-top: 20px;
}

#preview {
  max-width: 100%;
  height: auto;
}
</style>

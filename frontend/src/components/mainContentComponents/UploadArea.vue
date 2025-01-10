<template>
  <div class="upload-area" @click="triggerFileInput">
    <input type="file" ref="fileInput" multiple @change="uploadFiles" hidden />
    <div class="placeholder">
      <img :src="previewImage" alt="Preview" />
      <p class="text-black">Нажмите, чтобы загрузить фотографии</p>
    </div>
  </div>
</template>
  
  <script>
  export default {
    props: {
      previewImage: String,
    },
    methods: {
      triggerFileInput() {
        this.$refs.fileInput.click();
      },
      uploadFiles(event) {
        this.$emit('upload', event);
      },
    },
  };
  </script>


<style scoped>
.upload-area {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 400px;
  height: 300px;
  border: 2px dashed #ccc;
  cursor: pointer;
  background: #f9f9f9;
  text-align: center;
  border-radius: 10px;
}

.upload-area img {
  margin-bottom: 10px;
  width: 150px;
}

.placeholder {
  color: rgba(255, 255, 255, 0);
  font-size: 14px;
  text-align: center;
  justify-content: center;
  align-items: center;
}

</style>
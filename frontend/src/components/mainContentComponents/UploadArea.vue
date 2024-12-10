<template>
    <div class="upload-area" @click="triggerFileInput">
      <input type="file" ref="fileInput" multiple @change="uploadFiles" hidden />
      <div class="placeholder">
        <img :src="previewImage" alt="Preview" />
        Нажмите, чтобы загрузить фотографии
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
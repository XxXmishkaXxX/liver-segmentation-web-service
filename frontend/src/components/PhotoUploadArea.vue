<template>
    <div>
      <div class="upload-area" @click="triggerFileInput">
        <input type="file" ref="fileInput" multiple @change="handleFileSelect" hidden />
        <div v-if="!photos.length" class="placeholder">Нажмите, чтобы загрузить фотографии</div>
        <div v-else class="preview">
          <img :src="showBefore ? selectedPhoto.original : selectedPhoto.processed" alt="Preview" />
          <div class="mask" v-if="!showBefore"></div>
        </div>
      </div>
      <div class="toggle">
        <label>
          <input type="checkbox" v-model="localShowBefore" @change="emitToggle" />
          Показывать "до"
        </label>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      photos: Array,
      selectedPhoto: Object,
      showBefore: Boolean,
    },
    data() {
      return {
        localShowBefore: this.showBefore,
      };
    },
    methods: {
      triggerFileInput() {
        this.$refs.fileInput.click();
      },
      handleFileSelect(event) {
        const files = Array.from(event.target.files);
        const processedFiles = files.map((file) => {
          const reader = new FileReader();
          return new Promise((resolve) => {
            reader.onload = (e) => {
              resolve({
                original: e.target.result,
                processed: e.target.result,
                thumbnail: e.target.result,
              });
            };
            reader.readAsDataURL(file);
          });
        });
        Promise.all(processedFiles).then((uploadedFiles) => {
          this.$emit("file-upload", uploadedFiles);
        });
      },
      emitToggle() {
        this.$emit("toggle-before-after", this.localShowBefore);
      },
    },
  };
  </script>
  
  <style scoped>
  .upload-area {
    width: 300px;
    height: 300px;
    border: 2px dashed #ccc;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    margin-bottom: 20px;
  }
  .upload-area .placeholder {
    text-align: center;
    color: #aaa;
  }
  .upload-area .preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  .upload-area .preview .mask {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.3);
  }
  .toggle {
    margin-bottom: 20px;
  }
  </style>
  
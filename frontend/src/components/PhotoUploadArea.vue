<template>
    <div class="main-content">
      <div class="upload-area" @click="triggerFileInput">
        <input
          type="file"
          ref="fileInput"
          multiple
          @change="handleFileUpload"
          hidden
        />
        <div v-if="!photos.length" class="placeholder">
          Нажмите, чтобы загрузить фотографии
        </div>
        <div v-else class="preview">
          <img
            :src="photos[0]?.url"
            alt="Preview"
          />
        </div>
      </div>
      <div v-if="loading" class="loading-spinner">Загрузка...</div>
      <div v-if="uploadError" class="error-message">{{ uploadError }}</div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        photos: [], // Список загруженных фотографий
        loading: false, // Состояние загрузки
        uploadError: null, // Ошибка загрузки
      };
    },
    methods: {
      triggerFileInput() {
        this.$refs.fileInput.click();
      },
      async handleFileUpload(event) {
        const files = Array.from(event.target.files);
        if (!files.length) return;
  
        const formData = new FormData();
        files.forEach((file) => {
          formData.append('files', file); // `image` - поле на бэке
        });
        console.log(formData.files)
        try {
          this.loading = true;
          this.uploadError = null;
  
          // Отправка файлов на сервер
          const response = await this.$api.post('upload/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
  
          // Обновляем список фотографий после успешной загрузки
          this.photos.push(...response.data);
        } catch (error) {
          console.error('Ошибка загрузки изображений:', error);
          this.uploadError = 'Не удалось загрузить изображения. Попробуйте снова.';
        } finally {
          this.loading = false;
        }
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
  
  .loading-spinner {
    color: #007bff;
    font-size: 14px;
  }
  
  .error-message {
    color: red;
    font-size: 14px;
  }
  </style>
  
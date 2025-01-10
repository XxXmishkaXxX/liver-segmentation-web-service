<template>
  <div class="main-content">
    <UploadArea
      v-if="!masks.length && !loadingUpload && !loadingPredict"
      @upload="handleFileUpload"
      :previewImage="previewImage"
    />
    <ImagePreview
      v-else-if="masks.length && !loadingUpload && !loadingPredict && !isEditing"
      :masks="masks"
      :selectedMaskIndex="selectedMaskIndex"
      :currentMask="currentMask"
      :hasMoreMasks="hasMoreMasks"
      @prevMask="prevMask"
      @nextMask="nextMask"
      @editMask="editMask"
      @clearArrMasks="clearArr"
    />
    <MaskEditor
      v-if="isEditing"
      :backgroundImageUrl="currentMask.originalUrl"
      :maskUrl="currentMask.maskUrl"
      :initialMaskUrl="null" 
      @save="saveEditedMask"
      @close="isEditing = false"
    />
    <SpinnerLoader v-if="loadingUpload || loadingPredict" />
  </div>
</template>

<script>
import UploadArea from './mainContentComponents/UploadArea.vue';
import ImagePreview from './mainContentComponents/ImagePreview.vue';
import SpinnerLoader from './mainContentComponents/SpinnerLoader.vue';
import MaskEditor from './mainContentComponents/MaskEditor.vue';
import { toastMixin } from '../mixins/notifications';

export default {
  mixins: [toastMixin],
  components: { UploadArea, ImagePreview, MaskEditor, SpinnerLoader },
  data() {
    return {
      masks: [],
      selectedMaskIndex: 0,
      loadingUpload: false,
      loadingPredict: false,
      batch_id: null,
      task_id: null,
      previewImage: new URL('../assets/dcm-icon.png', import.meta.url),
      nextUrl: null,
      hasMoreMasks: true,
      isEditing: false,
    };
  },
  computed: {
    currentMask() {
      return this.masks[this.selectedMaskIndex] || { id: null, maskUrl: '', originalUrl: '' };
    },
  },
  methods: {
    clearArr() {
      this.masks = [];
    },
    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    async handleFileUpload(event) {
      const files = Array.from(event.target.files);
      if (!files.length) return;

      const formData = new FormData();
      files.forEach((file) => {
        formData.append('files', file);
      });

      try {
        this.loadingUpload = true;
        this.uploadError = null;

        const response = await this.$api.post('upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        this.batch_id = response.data.id;
        if (this.batch_id) {
          await this.predictBatch();
        }
      } catch (error) {
        console.error('Ошибка загрузки изображений:', error);
        this.uploadError = 'Не удалось загрузить изображения. Попробуйте снова.';
      } finally {
        this.loadingUpload = false;
      }
    },

    async predictBatch() {
      try {
        this.loadingPredict = true;
        const response = await this.$api.get(`batch/${this.batch_id}/predict/`);
        this.task_id = response.data.task_id;
        if (this.task_id) {
          this.checkTaskStatus();
        }
      } catch (error) {
        console.error('Ошибка запуска предсказания:', error);
        this.uploadError = 'Не удалось запустить предсказание.';
      } 
    },

    async checkTaskStatus() {
      const interval = setInterval(async () => {
        try {
          const response = await this.$api.get(`task-status/${this.task_id}/`);
          if (response.data.status === 'SUCCESS') {
            clearInterval(interval);
            this.$emit("add-batch-in-sidebar");
            this.showSuccessMessage('Модель успешно создала маски для ваших снимков')
            await this.getBatchResults();
            this.loadingPredict = false;
          } else if (response.data.status === 'FAILURE') {
            clearInterval(interval);
            this.showErrorMessage('произошла ошибка при создании масок')
            this.loadingPredict = false;
          }
        } catch (error) {
          console.error('Ошибка проверки статуса задачи:', error);
          this.showErrorMessage('Произошла ошибка при создании масок')
          clearInterval(interval);
          this.loadingPredict = false;
        }
      }, 3000);
    },

    async getBatchResults() {
      try {
        const response = await this.$api.get(`batch/${this.batch_id}/images/`);
        this.masks = response.data.results.map((item) => ({
            id: item.mask[1],
            maskUrl: item.mask[0],
            originalUrl: item.original[0],
          }));
        this.nextUrl = response.data.next;
        this.hasMoreMasks = !!this.nextUrl;
        this.selectedMaskIndex = 0;
      } catch (error) {
        console.error('Ошибка получения результатов:', error);
        this.uploadError = 'Не удалось получить результаты.';
      }
    },

    async nextMask() {
      if (this.selectedMaskIndex < this.masks.length - 1) {
        this.selectedMaskIndex++;
      } else if (this.hasMoreMasks && this.nextUrl) {
        await this.fetchNextMasks();
      }
    },

    prevMask() {
      if (this.selectedMaskIndex > 0) {
        this.selectedMaskIndex--;
      }
    },

    async fetchNextMasks() {
      try {
        this.loadingUpload = true;
        const response = await this.$api.get(this.nextUrl);
        const newMasks = response.data.results.map((item) => ({
          id: item.mask[1],
          maskUrl: item.mask[0],
          originalUrl: item.original[0],
        }));

        this.masks.push(...newMasks);
        this.nextUrl = response.data.next;

        if (!this.nextUrl) {
          this.hasMoreMasks = false;
        }
      } catch (error) {
        console.error('Ошибка загрузки следующей порции масок:', error);
        this.uploadError = 'Не удалось загрузить следующую порцию масок.';
      } finally {
        this.loadingUpload = false;
      }
    },
    editMask(maskId) {
      console.log('Редактирование маски с ID:', maskId);
      const mask = this.masks.find((m) => m.id === maskId);
      if (mask) {
        this.isEditing = true;
      } else {
        console.error('Маска не найдена!');
      }
    },
    openMaskEditor() {
      this.isEditing = true;
    },
    async saveEditedMask(newMaskData) {
      try {
        if (newMaskData.startsWith('data:image')) {
          const base64String = newMaskData.split(';base64,')[1];
          const byteCharacters = atob(base64String);
          const byteArrays = [];

          for (let offset = 0; offset < byteCharacters.length; offset += 1024) {
            const slice = byteCharacters.slice(offset, offset + 1024);
            const byteNumbers = new Array(slice.length);
            for (let i = 0; i < slice.length; i++) {
              byteNumbers[i] = slice.charCodeAt(i);
            }
            byteArrays.push(new Uint8Array(byteNumbers));
          }

          const blob = new Blob(byteArrays, { type: 'image/png' });
          const file = new File([blob], 'new_mask.png', { type: 'image/png' });

          const formData = new FormData();
          formData.append('new_mask', file);

          const response = await this.$api.put(
            `/update-mask/${this.currentMask.id}/`,
            formData,
            {
              headers: {
                'Content-Type': 'multipart/form-data'}
            }
          );

          console.log('Маска сохранена:', response.data);
          this.isEditing = false;

          this.masks.find((mask) => mask.id === this.currentMask.id).maskUrl = response.data.newMaskUrl;
        } 
      } catch (error) {
        console.error('Ошибка сохранения маски:', error);
      }
    },
  },
};
</script>

<style scoped>
.preview {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.carousel {
  display: flex;
  align-items: center;
  gap: 10px;
}

.carousel img {
  width: 300px;
  height: 300px;
  object-fit: contain;
}

.mask-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.error-message {
  color: red;
  text-align: center;
}

.status-message {
  text-align: center;
  color: green;
}

.main-content {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  padding: 20px;
}
</style>

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
    />
    <MaskEditor
      v-if="isEditing"
      :backgroundImageUrl="currentMask.maskUrl"
      :initialMaskUrl="null" 
      @save="saveEditedMask"
      @close="isEditing = false"
      />
    <SpinnerLoader v-if="loadingUpload || loadingPredict" />
    <StatusMessages
      v-if="statusMessage || uploadError"
      :statusMessage="statusMessage"
      :uploadError="uploadError"
    />
  </div>
</template>

<script>
import UploadArea from './mainContentComponents/UploadArea.vue';
import ImagePreview from './mainContentComponents/ImagePreview.vue';
import SpinnerLoader from './mainContentComponents/SpinnerLoader.vue';
import StatusMessages from './mainContentComponents/StatusMessages.vue';
import MaskEditor from './mainContentComponents/MaskEditor.vue';

export default {
  components: { UploadArea, ImagePreview, MaskEditor, SpinnerLoader, StatusMessages },
  data() {
    return {
      masks: [], // Список масок (фотографий)
      selectedMaskIndex: 0, // Индекс текущей маски
      loadingUpload: false, // Статус загрузки файлов
      loadingPredict: false, // Статус предикта
      uploadError: null, // Ошибка загрузки
      statusMessage: null, // Сообщение о статусе
      batch_id: null, // ID текущего батча
      task_id: null, // ID задачи
      previewImage: require('../assets/images/dcm-file-document-icon-vector-24678549.jpg'),
      nextUrl: null, // URL для загрузки следующей порции масок
      hasMoreMasks: true, // Флаг, есть ли еще маски
      isEditing: false,
    };
  },
  computed: {
    currentMask() {
      return this.masks[this.selectedMaskIndex] || { id: null, maskUrl: '' };
    },
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click(); // Инициализация загрузки файлов
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
          await this.predictBatch(); // Запуск предсказания для нового батча
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
          this.checkTaskStatus(); // Проверка статуса задачи
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
        this.statusMessage = 'Предсказание успешно завершено!';
        await this.getBatchResults(); // Получение результатов по завершению задачи
        this.loadingPredict = false; // Выключаем индикатор загрузки
      } else if (response.data.status === 'FAILURE') {
        clearInterval(interval);
        this.uploadError = 'Ошибка при обработке задач.';
        this.loadingPredict = false; // Выключаем индикатор загрузки
      }
    } catch (error) {
      console.error('Ошибка проверки статуса задачи:', error);
      this.uploadError = 'Не удалось проверить статус задачи.';
      clearInterval(interval);
      this.loadingPredict = false; // Выключаем индикатор загрузки в случае ошибки
    }
  }, 3000); // Проверяем статус каждые 3 секунды
},

    async getBatchResults() {
      try {
        const response = await this.$api.get(`batch/${this.batch_id}/images/`);
        this.masks = response.data.results.map((item) => ({
          id: item.mask[1],
          maskUrl: item.mask[0],
        }));
        this.nextUrl = response.data.next;
        this.hasMoreMasks = !!this.nextUrl;
        this.selectedMaskIndex = 0; // Сброс индекса на 0 для отображения первой маски
      } catch (error) {
        console.error('Ошибка получения результатов:', error);
        this.uploadError = 'Не удалось получить результаты.';
      }
    },

    async nextMask() {
      if (this.selectedMaskIndex < this.masks.length - 1) {
        this.selectedMaskIndex++;
      } else if (this.hasMoreMasks && this.nextUrl) {
        await this.fetchNextMasks(); // Загрузка следующей порции масок
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
        }));

        this.masks.push(...newMasks); // Добавляем новые маски в список
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
      this.isEditing = true; // Включаем редактор
    } else {
      console.error('Маска не найдена!');
    }
  },
    openMaskEditor(maskId) {
      this.isEditing = true;
    },
    async saveEditedMask(newMaskData) {
  try {
    // Проверим, если строка Base64 начинается с префикса 'data:image'
    if (newMaskData.startsWith('data:image')) {
      // Отрезаем префикс 'data:image/*;base64,' для получения чистой строки Base64
      const base64String = newMaskData.split(';base64,')[1];

      // Декодируем Base64 в бинарные данные
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

      // Создаем объект Blob из бинарных данных
      const blob = new Blob(byteArrays, { type: 'image/png' }); // Убедитесь, что тип соответствует вашему изображению

      // Создаем файл из Blob
      const file = new File([blob], 'new_mask.png', { type: 'image/png' });

      // Создаем FormData и добавляем файл
      const formData = new FormData();
      formData.append('new_mask', file);

      // Отправляем PUT запрос с FormData
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

      // Обновить маску в списке
      const updatedMask = this.masks.find((mask) => mask.id === this.currentMask.id);
      if (updatedMask) {
        updatedMask.maskUrl = response.data.maskUrl; // Пример обновления URL маски
      }
    } else {
      console.error('Invalid image format');
    }
  } catch (error) {
    console.error('Ошибка сохранения маски:', error);
  }
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
  height: 100px;
  margin-bottom: 10px;
}

.placeholder {
  color: #888;
  font-size: 14px;
}

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
</style>

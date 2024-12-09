<template>
  <div class="main-content">
    <!-- Область загрузки -->
    <div v-if="!masks.length && !loading" class="upload-area" @click="triggerFileInput">
      <input
        type="file"
        ref="fileInput"
        multiple
        @change="handleFileUpload"
        hidden
      />
      <div v-if="!masks.length" class="placeholder">
        <img :src="previewImage" alt="Preview" style="height: 200px;" />
        Нажмите, чтобы загрузить фотографии
      </div>
    </div>

    <!-- Превью изображений (если маски загружены) -->
    <div v-else class="preview">
      <div class="carousel">
        <button @click.stop="prevMask" :disabled="selectedMaskIndex === 0">
          ⬅️
        </button>
        <div class="mask-preview">
          <img :src="currentMask.maskUrl" alt="Mask Preview" />
          <p>ID маски: {{ currentMask.id }}</p>
          <button @click.stop="editMask(currentMask.id)">Редактировать</button>
        </div>
        <button
          @click.stop="nextMask"
          :disabled="!hasMoreMasks && selectedMaskIndex === masks.length - 1"
        >
          ➡️
        </button>
      </div>
    </div>

    <!-- Лоадер и ошибки -->
    <div v-if="loading" class="loading-spinner">Загрузка...</div>
    <div v-if="uploadError" class="error-message">{{ uploadError }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      masks: [], // Список масок (фотографий)
      selectedMaskIndex: 0, // Индекс текущей маски
      loading: false, // Статус загрузки
      uploadError: null, // Ошибка загрузки
      batch_id: null, // ID текущего батча
      task_id: null, // ID задачи
      previewImage: require('../assets/images/dcm-file-document-icon-vector-24678549.jpg'),
      nextUrl: null, // URL для загрузки следующей порции масок
      hasMoreMasks: true, // Флаг, есть ли еще маски
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
        this.loading = true;
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
        this.loading = false;
      }
    },

    async predictBatch() {
      try {
        const response = await this.$api.get(`batch/${this.batch_id}/predict/`);
        this.task_id = response.data.task_id;
        if (this.task_id) {
          this.checkTaskStatus(); // Проверка статуса задачи
        }
      } catch (error) {
        console.error('Ошибка запуска предсказания:', error);
      }
    },

    async checkTaskStatus() {
      const interval = setInterval(async () => {
        try {
          const response = await this.$api.get(`task-status/${this.task_id}/`);
          if (response.data.status === 'SUCCESS') {
            clearInterval(interval);
            this.$emit("add-batch-in-sidebar")
            await this.getBatchResults(); // Получение результатов по завершению задачи
          } else if (response.data.status === 'FAILURE') {
            clearInterval(interval);
            this.uploadError = 'Ошибка при обработке задач.';
          }
        } catch (error) {
          console.error('Ошибка проверки статуса задачи:', error);
          this.uploadError = 'Не удалось проверить статус задачи.';
        }
      }, 3000); // Проверка статуса задачи каждые 3 секунды
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
        this.loading = true;
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
        this.loading = false;
      }
    },

    editMask(maskId) {
      // Логика для редактирования маски
      console.log('Редактирование маски с ID:', maskId);
    },
  },
};
</script>

<style scoped>
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

.upload-area {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  border: 1px dashed #ccc;
  cursor: pointer;
}

.placeholder {
  text-align: center;
  color: #888;
}

.mask-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.loading-spinner {
  text-align: center;
  color: #666;
}

.error-message {
  color: red;
  text-align: center;
}
</style>

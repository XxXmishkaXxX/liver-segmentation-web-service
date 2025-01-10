<template>
  <div class="batch-sidebar">
    <h3 class="text-white fixed-header">Ваши батчи</h3>
    <div class="scrollable-content">
      <ul class="mt-5">
        <li v-for="batch in batches" :key="batch.id" class="batch-item mb-3 p-2">
          <div class="batch-info" @click="selectBatch(batch.id)">
            <img :src="batch.first_img.image_url" alt="Batch Preview" class="batch-image" />
            <div>
              <p class="batch-date">Дата создания: {{ formatDate(batch.created_at) }}</p>
              <p class="batch-count">Количество фото: {{ batch.image_count }}</p>
            </div>
          </div>
          <div class="action-buttons">
            <button class="btn btn-success" @click.stop="openModal(batch.id)">
              <i class="fas fa-download"></i>
            </button>
            <button class="btn btn-danger" @click.stop="deleteBatch(batch.id)">
              <i class="fas fa-trash-alt"></i>
            </button>
          </div>
        </li>
      </ul>
      <div v-if="loading" class="loading">Загрузка...</div>
      <div v-if="error" class="error">{{ error }}</div>
    </div>
  </div>

  <!-- Модальное окно для выбора опций скачивания -->
  <div v-if="isModalOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <h3>Выберите опции для скачивания</h3>
      <div>
        <input type="checkbox" v-model="includeOverlay" id="include-overlay">
        <label for="include-overlay">Маски поверх оригинала</label>
      </div>
      <div class="modal-actions">
        <button class="btn btn-secondary" @click="closeModal">Закрыть</button>
        <button class="btn btn-success" @click="downloadBatchWithOptions">Скачать</button>
      </div>
    </div>
  </div>

  <!-- Спиннер (колесо ожидания) -->
  <div v-if="isDownloading" class="loading-overlay">
    <div class="spinner"></div>
    Загрузка...
  </div>
</template>



<script>
export default {
  data() {
    return {
      batches: [],
      loading: false,
      error: null,
      isModalOpen: false,
      isDownloading: false,  // Флаг для отображения спиннера
      selectedBatchId: null,
      includeOverlay: false,  // Для хранения состояния чекбокса
    };
  },
  methods: {
    async getBatches() {
      this.loading = true;
      this.error = null;
      try {
        const response = await this.$api.get('batches/');
        this.batches = response.data;
      } catch {
        this.error = "Не удалось загрузить батчи.";
      } finally {
        this.loading = false;
      }
    },
    openModal(batchId) {
      this.selectedBatchId = batchId;
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },
    async downloadBatchWithOptions() {
      this.closeModal();
      this.isDownloading = true;  // Показываем спиннер
      try {
        const url = `batch/${this.selectedBatchId}/download/?include_overlay=${this.includeOverlay}`;
        const response = await this.$api.get(url, { responseType: 'blob' });
        
        // Создаем ссылку для скачивания
        const urlBlob = URL.createObjectURL(response.data);
        const a = document.createElement('a');
        a.href = urlBlob;
        a.download = `masks_${this.selectedBatchId}.zip`;
        a.click();
        
      } catch {
        alert("Не удалось скачать батч.");
      } finally {
        this.isDownloading = false;  // Скрываем спиннер после завершения загрузки
      }
    },
    selectBatch(batchId) {
      this.$emit("select-batch", batchId);
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('ru-RU', {
        year: 'numeric', month: 'long', day: 'numeric'
      });
    },
  },
  mounted() {
    this.getBatches();
  },
};
</script>


<style scoped>
.batch-sidebar {
  width: 300px;
  padding: 20px 0;
  background: rgba(255, 255, 255, 0);
  display: flex;
  flex-direction: column;
  height: 100%;
  border-right: 2px solid white;
}
.fixed-header {
  flex-shrink: 0;
  margin-bottom: 10px;
}
.scrollable-content {
  flex-grow: 1;
  overflow-y: auto;
  padding-right: 30px;
  scrollbar-width: none;
}
.batch-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #ddd;
  background-color: white;
  border-radius: 15px;
}
.batch-info {
  display: flex;
  align-items: center;
}
.batch-image {
  width: 50px;
  height: 50px;
  border-radius: 5px;
  margin-right: 10px;
  object-fit: cover;
}
.batch-date, .batch-count {
  font-size: 12px;
  color: #666;
}
.action-buttons {
  display: block;
}
.action-buttons button {
  margin-bottom: 5px;
}

.loading {
  text-align: center;
  color: #666;
}
.error {
  color: red;
  text-align: center;
}

/* Стили для модального окна */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 400px;
  text-align: center;
}

.modal-actions {
  margin-top: 20px;
}

.modal-actions button {
  margin: 0 10px;
}

/* Стили для спиннера */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.spinner {
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid #fff;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>

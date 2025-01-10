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
            <button class="btn btn-success" @click.stop="downloadBatch(batch.id)">
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
</template>

<script>
export default {
  data() {
    return {
      batches: [],
      loading: false,
      error: null,
      isModalOpen: false,
      previewImage: require('../assets/images/dcm-file-document-icon-vector-24678549.jpg'),
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
    openUploadModal() {
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },
    async handleFileUpload(event) {
      const files = Array.from(event.target.files);
      if (!files.length) return;

      const formData = new FormData();
      files.forEach(file => formData.append('files', file));

      this.loading = true;
      this.error = null;
      try {
        const response = await this.$api.post('upload/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        this.batch_id = response.data.id;
        if (this.batch_id) await this.predictBatch();
      } catch {
        this.error = 'Не удалось загрузить изображения. Попробуйте снова.';
      } finally {
        this.loading = false;
        this.closeModal();
      }
    },
    async deleteBatch(batchId) {
      if (!confirm("Вы уверены, что хотите удалить этот батч?")) return;

      this.loading = true;
      try {
        await this.$api.delete(`delete-batch/${batchId}/`);
        this.batches = this.batches.filter(batch => batch.id !== batchId);
        this.$emit("clear-preview-area", batchId);
      } catch {
        alert("Не удалось удалить батч.");
      } finally {
        this.loading = false;
      }
    },
    async downloadBatch(batchId) {
      try {
        const response = await this.$api.get(`batches/${batchId}/download/`, { responseType: 'blob' });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `batch-${batchId}.zip`);
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch {
        alert("Не удалось скачать батч.");
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
  width: 100%;
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
</style>


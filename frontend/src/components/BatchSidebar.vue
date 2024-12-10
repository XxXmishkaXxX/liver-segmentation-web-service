<template>
  <div class="batch-sidebar">
    <h3>Ваши батчи</h3>
    <ul>
      <li v-for="batch in batches" :key="batch.id" class="batch-item">
        <div class="batch-info" @click="selectBatch(batch.id)">
          <img :src="batch.first_mask.image_file" alt="Batch Preview" class="batch-image" />
          <div>
            <p class="batch-date">Дата создания: {{ formatDate(batch.created_at) }}</p>
            <p class="batch-count">Количество фото: {{ batch.image_count }}</p>
          </div>
        </div>
        <button class="delete-btn" @click="deleteBatch(batch.id)">Удалить</button>
      </li>
    </ul>
    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      batches: [], // Список батчей
      loading: false,
      error: null,
    };
  },
  methods: {
    async getBatches() {
      try {
        this.loading = true;
        this.error = null;

        // Получаем данные о батчах с API
        const response = await this.$api.get('batches/');
        this.batches = response.data;
      } catch (err) {
        this.error = "Не удалось загрузить батчи.";
      } finally {
        this.loading = false;
      }
    },
    async deleteBatch(batchId) {
      try {
        if (!confirm("Вы уверены, что хотите удалить этот батч?")) return;

        this.loading = true;
        await this.$api.delete(`delete-batch/${batchId}/`);
        this.batches = this.batches.filter((batch) => batch.id !== batchId);

        // Передаем id удаленного батча родителю
        this.$emit("clear-preview-area", batchId);
      } catch (err) {
        alert("Не удалось удалить батч.");
      } finally {
        this.loading = false;
      }
    },
    async selectBatch(batchId) {
      this.$emit("select-batch", batchId); // Передаем выбранный батч родительскому компоненту
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('ru-RU', options);
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
  background: #f4f4f4;
  padding: 10px;
  overflow-y: auto;
}

.batch-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #ddd;
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

.batch-name {
  font-weight: bold;
  cursor: pointer;
}

.batch-date,
.batch-count {
  font-size: 12px;
  color: #666;
}

.delete-btn {
  background: #ff4d4f;
  color: white;
  border: none;
  padding: 5px;
  cursor: pointer;
  border-radius: 3px;
}

.delete-btn:hover {
  background: #d9363e;
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

<template>
  <div class="workspace">
    <BatchSidebar class="sidebar" 
                  ref="sideBar" 
                  @select-batch="selectBatch"
                  @clear-preview-area="clearPreviewArea" />
    <BatchDetail ref="batchDetail" @add-batch-in-sidebar="addBatchInSideBar" />
  </div>
</template>

<script>
import BatchSidebar from "../components/BatchSidebar.vue";
import BatchDetail from "../components/BatchDetail.vue";

export default {
  components: {
    BatchSidebar,
    BatchDetail,
  },
  methods: {
    async selectBatch(batch_id) {
      if (this.$refs.batchDetail) {
        this.$refs.batchDetail.batch_id = batch_id;
        this.$refs.batchDetail.getBatchResults();
      } else {
        console.error('Компонент BatchDetail еще не доступен');
      }
    },
    async addBatchInSideBar() {
      if (this.$refs.sideBar) {
        this.$refs.sideBar.getBatches();
      }
    },
    async clearPreviewArea(deletedBatchId) {
      if (this.$refs.batchDetail.batch_id === deletedBatchId) {
        console.log("Удаляем текущий просматриваемый батч, очищаем зону превью");
        this.$refs.batchDetail.masks = [];
        this.$refs.batchDetail.batch_id = null; // Сбрасываем текущий ID батча
      } else {
        console.log("Удален другой батч, зона превью не очищается");
      }
}
  },
};
</script>

<style scoped>
.workspace {
  position: relative;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  position: absolute; /* Абсолютное позиционирование */
  top: 0;
  left: 0;
  width: 300px; /* Ширина сайдбара */
  height: 100%; /* Занимает всю высоту */
  background: #f4f4f4;
  z-index: 10; /* Поверх основного контента */
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}
.main-content {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  padding: 20px;
  margin-left: 300px; /* Отступ слева, равный ширине сайдбара */
  background: #fff;
}
</style>

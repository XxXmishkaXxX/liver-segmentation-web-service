<template>
  <div class="workspace d-flex">
    <BatchSidebar class="sidebar" 
                ref="sideBar" 
                @select-batch="selectBatch"
                @clear-preview-area="clearPreviewArea" />
    <BatchDetail ref="batchDetail" class="detail" @add-batch-in-sidebar="addBatchInSideBar" />
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
  display: flex;
  height: 100vh;
  padding: 20px;
  gap: 20px; /* Расстояние между колонками */
  background-image: url('@/assets/img/workspace/background.svg');
}

.sidebar {

  flex: 0 0 300px; /* Фиксированная ширина для сайдбара */
  height: 100%;
  background: rgba(255, 255, 255, 0);
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  scrollbar-width: none;

}

.detail {
  flex: 1; /* Займет оставшееся пространство */
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}


</style>

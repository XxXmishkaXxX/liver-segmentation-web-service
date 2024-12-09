<template>
  <div class="workspace">
    <!-- Сайдбар с батчами -->
    <BatchSidebar class="sidebar" ref="sideBar" @select-batch="selectBatch" />

    <!-- Основной контент -->
    <div class="main-content">
      <!-- Область загрузки -->
      <BatchDetail ref="batchDetail" @add-batch-in-sidebar="addBatchInSideBar"/>
    </div>
  </div>
</template>

<script>
import BatchSidebar from "../components/BatchSidebar.vue"; // Компонент сайдбара
import BatchDetail from "../components//BatchDetail.vue"; // Компонент загрузки фотографий

export default {
  components: {
    BatchSidebar,
    BatchDetail,
  },
  data() {
    return {
    };
  },
  computed: {
  },
  methods: {

    async selectBatch(batch_id){
      if (this.$refs.batchDetail) {
      this.$refs.batchDetail.batch_id = batch_id;
      this.$refs.batchDetail.getBatchResults();
    } else {
      console.error('Компонент BatchDetail еще не доступен');
    }
    },

    async addBatchInSideBar() {
      if (this.$refs.sideBar){
        this.$refs.sideBar.getBatches()
      }

    }

  },
};
</script>

<style scoped>
.workspace {
  display: flex;
  height: 100vh;
}
.sidebar {
  width: 20%;
  background: #f4f4f4;
  padding: 10px;
  overflow-y: auto;
}
.main-content {
  width: 80%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>

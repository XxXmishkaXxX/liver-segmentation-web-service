<template>
  <div class="workspace">
    <!-- Сайдбар с батчами -->
    <BatchSidebar class="sidebar" @select-batch="selectBatch" />

    <!-- Основной контент -->
    <div class="main-content">
      <!-- Область загрузки -->
      <PhotoUploadArea
        :photos="photos"
        :selected-photo="selectedPhoto"
        :show-before="showBefore"
        @file-upload="handleFileUpload"
        @toggle-before-after="toggleBeforeAfter"
      />
    </div>
  </div>
</template>

<script>
import BatchSidebar from "../components/BatchSidebar.vue"; // Компонент сайдбара
import PhotoUploadArea from "../components//PhotoUploadArea.vue"; // Компонент загрузки фотографий

export default {
  components: {
    BatchSidebar,
    PhotoUploadArea,
  },
  data() {
    return {
      photos: [], // Список загруженных фотографий
      selectedPhotoIndex: 0, // Индекс выбранной фотографии
      showBefore: true, // Тумблер "до/после"
      currentPage: 1, // Текущая страница пагинации
      photosPerPage: 5, // Количество фотографий на странице
    };
  },
  computed: {
    selectedPhoto() {
      return this.photos[this.selectedPhotoIndex] || {};
    },
  },
  methods: {
    selectBatch(batchId) {
      console.log("Выбран батч:", batchId);
      // Обработайте выбор батча, например, подгрузите фото
    },
    handleFileUpload(files) {
      const uploadedPhotos = files.map((file, index) => ({
        id: this.photos.length + index,
        original: file.original,
        processed: file.processed,
        thumbnail: file.thumbnail,
      }));
      this.photos.push(...uploadedPhotos);
    },
    selectPhoto(index) {
      this.selectedPhotoIndex = index;
    },
    toggleBeforeAfter(value) {
      this.showBefore = value;
    },
    handlePageChange(page) {
      this.currentPage = page;
    },
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

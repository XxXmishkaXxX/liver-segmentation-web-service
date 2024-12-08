<template>
    <div>
      <div class="photo-gallery">
        <div
          v-for="(photo, index) in photos"
          :key="photo.id"
          class="photo-thumbnail"
          @click="selectPhoto(index)"
        >
          <img :src="photo.thumbnail" />
        </div>
      </div>
      <div class="pagination">
        <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1">Назад</button>
        <span>Страница {{ currentPage }} из {{ totalPages }}</span>
        <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages">Вперед</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      photos: Array,
      currentPage: Number,
      totalPages: Number,
    },
    methods: {
      selectPhoto(index) {
        this.$emit("select-photo", index);
      },
      changePage(page) {
        this.$emit("change-page", page);
      },
    },
  };
  </script>
  
  <style scoped>
  .photo-gallery {
    display: flex;
    overflow-x: auto;
    gap: 10px;
  }
  .photo-thumbnail img {
    width: 80px;
    height: 80px;
    object-fit: cover;
    cursor: pointer;
    border: 2px solid transparent;
  }
  .photo-thumbnail img:hover {
    border: 2px solid #007bff;
  }
  .pagination {
    margin-top: 20px;
  }
  .pagination button {
    margin: 0 5px;
  }
  </style>
  
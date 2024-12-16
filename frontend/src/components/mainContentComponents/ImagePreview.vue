<template>
  <div class="preview">
    <div class="carousel">
      <!-- Кнопка для предыдущей маски -->
      <button @click="prevMask" :disabled="!hasPreviousMask" class="nav-button">
        ⬅️
      </button>
      
      <!-- Превью маски -->
      <div class="mask-preview">
        <div class="image-mask-container">
          <img :src="currentMask.originalUrl" alt="Original Image" class="original-image" />
          <img 
            v-if="showMask" 
            :src="currentMask.maskUrl" 
            alt="Mask Preview" 
            class="mask-image" 
          />
        </div>
        <p>ID маски: {{ currentMask.id }}</p>
        <button @click="editMask(currentMask.id)">Редактировать</button>
        <!-- Кнопка для показа/скрытия маски -->
        <button @click="toggleMask" class="toggle-mask-button">
          {{ showMask ? 'Скрыть маску' : 'Показать маску' }}
        </button>
      </div>
      
      <!-- Кнопка для следующей маски -->
      <button @click="nextMask" :disabled="!hasNextMask" class="nav-button">
        ➡️
      </button>
    </div>

    <!-- Сообщение при отсутствии масок -->
    <p v-if="!masks.length" class="no-masks-message">
      Маски отсутствуют.
    </p>
  </div>
</template>

<script>
export default {
  props: {
    masks: {
      type: Array,
      required: true,
    },
    selectedMaskIndex: {
      type: Number,
      required: true,
    },
    currentMask: {
      type: Object,
      required: true,
    },
    hasMoreMasks: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      showMask: true, // Управляет показом/скрытием маски
    };
  },
  computed: {
    hasPreviousMask() {
      return this.selectedMaskIndex > 0;
    },
    hasNextMask() {
      return this.selectedMaskIndex < this.masks.length - 1 || this.hasMoreMasks;
    },
  },
  methods: {
    prevMask() {
      this.$emit('prevMask');
    },
    nextMask() {
      this.$emit('nextMask');
    },
    editMask(maskId) {
      this.$emit('editMask', maskId);
    },
    toggleMask() {
      this.showMask = !this.showMask; // Переключаем состояние маски
    },
  },
};
</script>

<style scoped>
.carousel {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-button {
  background-color: #007bff;
  border: none;
  color: white;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 5px;
}

.nav-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.mask-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.image-mask-container {
  position: relative;
  display: inline-block;
  width: 300px;
  height: 300px;
}

.original-image,
.mask-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.toggle-mask-button {
  margin-top: 10px;
  padding: 5px 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.toggle-mask-button:hover {
  background-color: #218838;
}

.no-masks-message {
  text-align: center;
  color: #888;
  font-size: 16px;
  margin-top: 20px;
}
</style>

<template>
  <div class="mask-editor">
    <div class="image-container" :style="{ backgroundImage: 'url(' + backgroundImageUrl + ')' }">
      <canvas
        ref="canvas"
        class="canvas"
        @mousedown="handleMouseDown"
        @mousemove="handleMouseMove"
        @mouseup="stopDrawing"
        @mouseleave="stopDrawing"
      ></canvas>
    </div>
    <div class="controls">
      <label>
        {{ isErasing ? 'Толщина ластика' : 'Толщина кисти' }}:
        <input type="range" v-model="currentBrushSize" min="1" max="50" />
        {{ currentBrushSize }}
      </label>
      <button @click="toggleEraser">{{ isErasing ? 'Кисть' : 'Ластик' }}</button>
      <button @click="undo">Отменить</button>
      <button @click="saveMask">Сохранить</button>
      <button @click="$emit('close')">Закрыть</button>
      <button @click="toggleMaskVisibility">{{ isMaskHidden ? 'Показать маску' : 'Скрыть маску' }}</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    maskUrl: String,
    backgroundImageUrl: String,
    initialMaskUrl: String,
  },
  data() {
    return {
      currentColor: '#00FF00',
      currentBrushSize: 5, // Размер ластика и кисти
      isDrawing: false,
      isErasing: false,
      isMaskHidden: false, // Новая переменная для управления видимостью маски
      canvasContext: null,
      lastPosition: null,
      history: [], // Стек для хранения состояний холста
    };
  },
  methods: {
    initCanvas() {
      const canvas = this.$refs.canvas;
      const container = this.$el.querySelector('.image-container');

      canvas.width = container.offsetWidth;
      canvas.height = container.offsetHeight;
      this.canvasContext = canvas.getContext('2d', { willReadFrequently: true });

      if (this.maskUrl) {
        const img = new Image();
        img.src = this.maskUrl;
        img.onload = () => {
          this.canvasContext.drawImage(img, 0, 0, canvas.width, canvas.height);
        };
      }
    },
    toggleMaskVisibility() {
      this.isMaskHidden = !this.isMaskHidden;
      const canvas = this.$refs.canvas;
      if (this.isMaskHidden) {
        canvas.style.visibility = 'hidden'; // Скрыть маску
      } else {
        canvas.style.visibility = 'visible'; // Показать маску
      }
    },
    saveState() {
      const canvas = this.$refs.canvas;
      this.history.push(this.canvasContext.getImageData(0, 0, canvas.width, canvas.height));
      // Ограничиваем стек до 20 действий
      if (this.history.length > 20) {
        this.history.shift();
      }
    },
    handleMouseDown(event) {
      this.saveState(); // Сохраняем состояние перед началом рисования
      this.isDrawing = true;
      const { x, y } = this.getMousePosition(event);
      this.lastPosition = { x, y };
    },
    handleMouseMove(event) {
      if (!this.isDrawing) return;
      const { x, y } = this.getMousePosition(event);
      this.drawLine(this.lastPosition.x, this.lastPosition.y, x, y);
      this.lastPosition = { x, y };
    },
    stopDrawing() {
      if (!this.isDrawing) return;
      this.isDrawing = false;
    },
    drawLine(x1, y1, x2, y2) {
      this.canvasContext.lineWidth = this.currentBrushSize;
      this.canvasContext.lineCap = 'round';

      if (this.isErasing) {
        // Ластик рисует круги
        this.canvasContext.clearRect(
          x1 - this.currentBrushSize / 2,
          y1 - this.currentBrushSize / 2,
          this.currentBrushSize,
          this.currentBrushSize
        );
      } else {
        // Рисуем линию кистью
        this.canvasContext.strokeStyle = this.currentColor;
        this.canvasContext.beginPath();
        this.canvasContext.moveTo(x1, y1);
        this.canvasContext.lineTo(x2, y2);
        this.canvasContext.stroke();
      }
    },
    getMousePosition(event) {
      const canvas = this.$refs.canvas;
      const rect = canvas.getBoundingClientRect();
      return {
        x: event.clientX - rect.left,
        y: event.clientY - rect.top,
      };
    },
    toggleEraser() {
      this.isErasing = !this.isErasing;
    },
    undo() {
      if (this.history.length === 0) return; // Если стек пуст, ничего не делаем

      const previousState = this.history.pop(); // Получаем последнее состояние
      this.canvasContext.putImageData(previousState, 0, 0); // Восстанавливаем его на холсте
    },
    saveMask() {
      const dataUrl = this.$refs.canvas.toDataURL();
      this.$emit('save', dataUrl);
    },
  },
  mounted() {
    this.initCanvas();
  },
};
</script>

<style scoped>
.mask-editor {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.image-container {
  position: relative;
  background-size: cover;
  background-position: center;
  width: 500px;
  height: 500px;
}

.canvas {
  border: 1px solid #ccc;
  cursor: crosshair;
  width: 100%;
  height: 100%;
}

.controls {
  margin-top: 10px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
</style>

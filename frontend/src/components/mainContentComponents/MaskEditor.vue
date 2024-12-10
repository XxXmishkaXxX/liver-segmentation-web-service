<template>
    <div class="mask-editor">
      <canvas
        ref="canvas"
        width="500"
        height="500"
        class="canvas"
        @mousedown="handleMouseDown"
        @mousemove="handleMouseMove"
        @mouseup="stopDrawing"
        @mouseleave="stopDrawing"
      ></canvas>
      <div class="controls">
        <label>
          Цвет кисти:
          <input type="color" v-model="currentColor" />
        </label>
        <label>
          Толщина кисти:
          <input type="range" v-model="currentBrushSize" min="1" max="50" />
          {{ currentBrushSize }}
        </label>
        <button @click="toggleEraser">{{ isErasing ? 'Кисть' : 'Ластик' }}</button>
        <button @click="undoLastAction">Отменить</button>
        <button @click="saveMask">Сохранить</button>
        <button @click="$emit('close')">Закрыть</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      backgroundImageUrl: String,
      initialMaskUrl: String,
    },
    data() {
      return {
        currentColor: '#000000',
        currentBrushSize: 5,
        isDrawing: false,
        isErasing: false,
        canvasContext: null,
        actionsStack: [],
        lastPosition: null,
        path: [], // Список для хранения координат пути
      };
    },
    methods: {
      initCanvas() {
        const canvas = this.$refs.canvas;
        this.canvasContext = canvas.getContext('2d', { willReadFrequently: true });
        if (this.backgroundImageUrl) {
          const img = new Image();
          img.src = this.backgroundImageUrl;
          img.onload = () => {
            this.canvasContext.drawImage(img, 0, 0, canvas.width, canvas.height);
          };
        }
      },
      saveCurrentState() {
        const snapshot = this.$refs.canvas.toDataURL();
        this.actionsStack.push(snapshot);
      },
      undoLastAction() {
        if (this.actionsStack.length > 0) {
          const previousState = this.actionsStack.pop();
          const img = new Image();
          img.src = previousState;
          img.onload = () => {
            this.canvasContext.clearRect(0, 0, this.$refs.canvas.width, this.$refs.canvas.height);
            this.canvasContext.drawImage(img, 0, 0, this.$refs.canvas.width, this.$refs.canvas.height);
          };
        }
      },
      handleMouseDown(event) {
        this.isDrawing = true;
        this.saveCurrentState(); // Сохраняем текущее состояние
        const { x, y } = this.getMousePosition(event);
        this.lastPosition = { x, y };
        this.path = [{ x, y }]; // Начинаем новый путь
      },
      handleMouseMove(event) {
        if (!this.isDrawing) return;
        const { x, y } = this.getMousePosition(event);
        this.drawLine(this.lastPosition.x, this.lastPosition.y, x, y);
        this.lastPosition = { x, y };
        this.path.push({ x, y }); // Добавляем координаты в путь
      },
      stopDrawing(event) {
        if (!this.isDrawing) return;
        this.isDrawing = false;
        this.canvasContext.closePath();
        this.checkForClosedPath(); // Проверка, замкнут ли путь
      },
      drawLine(x1, y1, x2, y2) {
        this.canvasContext.lineWidth = this.currentBrushSize;
        this.canvasContext.lineCap = 'round';
        this.canvasContext.strokeStyle = this.isErasing ? '#FFFFFF' : this.currentColor;
  
        this.canvasContext.beginPath();
        this.canvasContext.moveTo(x1, y1);
        this.canvasContext.lineTo(x2, y2);
        this.canvasContext.stroke();
      },
      checkForClosedPath() {
        const firstPoint = this.path[0];
        const lastPoint = this.path[this.path.length - 1];
        
        // Проверяем, замкнулся ли путь
        if (Math.abs(firstPoint.x - lastPoint.x) <= this.currentBrushSize && 
            Math.abs(firstPoint.y - lastPoint.y) <= this.currentBrushSize) {
          this.fillPath(); // Если замкнулся, заполняем область
        }
      },
      fillPath() {
        const { x, y } = this.path[0]; // Точка начала
        const targetColor = this.getPixelColor(x, y); // Цвет начальной точки
        if (targetColor !== this.currentColor) {
          this.floodFill(x, y, targetColor, this.hexToRgb(this.currentColor)); // Заполняем область
        }
      },
      floodFill(x, y, targetColor, replacementColor) {
        const canvas = this.$refs.canvas;
        const ctx = this.canvasContext;
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;
  
        const stack = [{ x, y }];
        const pixelIndex = (x, y) => (y * canvas.width + x) * 4;
  
        // Функция для проверки, совпадает ли цвет пикселя
        function isMatchingColor(x, y, color) {
          const i = pixelIndex(x, y);
          return (
            data[i] === color[0] &&
            data[i + 1] === color[1] &&
            data[i + 2] === color[2] &&
            data[i + 3] === color[3]
          );
        }
  
        // Функция для изменения цвета пикселя
        function setColor(x, y, color) {
          const i = pixelIndex(x, y);
          data[i] = color[0];
          data[i + 1] = color[1];
          data[i + 2] = color[2];
          data[i + 3] = color[3];
        }
  
        const targetColorArray = targetColor.split(',').map(Number);
        const replacementColorArray = replacementColor;
  
        while (stack.length) {
          const { x, y } = stack.pop();
          if (x < 0 || x >= canvas.width || y < 0 || y >= canvas.height) continue;
          if (isMatchingColor(x, y, targetColorArray)) {
            setColor(x, y, replacementColorArray);
            stack.push({ x: x + 1, y });
            stack.push({ x: x - 1, y });
            stack.push({ x, y: y + 1 });
            stack.push({ x, y: y - 1 });
          }
        }
        ctx.putImageData(imageData, 0, 0);
      },
      getPixelColor(x, y) {
        const canvas = this.$refs.canvas;
        const ctx = this.canvasContext;
        const pixel = ctx.getImageData(x, y, 1, 1).data;
        return `${pixel[0]},${pixel[1]},${pixel[2]},${pixel[3]}`; // Возвращаем цвет как строку
      },
      hexToRgb(hex) {
        const bigint = parseInt(hex.slice(1), 16);
        return [
          (bigint >> 16) & 255,
          (bigint >> 8) & 255,
          bigint & 255,
          255,
        ]; // Возвращаем в формате rgba
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
  }
  .canvas {
    border: 1px solid #ccc;
    cursor: crosshair;
  }
  .controls {
    margin-top: 10px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  </style>
  
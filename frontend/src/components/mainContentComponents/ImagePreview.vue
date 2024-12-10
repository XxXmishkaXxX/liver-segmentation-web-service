<template>
    <div class="preview">
      <div class="carousel">
        <button @click="prevMask" :disabled="!hasPreviousMask">⬅️</button>
        <div class="mask-preview">
          <img :src="currentMask.maskUrl" alt="Mask Preview" />
          <p>ID маски: {{ currentMask.id }}</p>
          <button @click="editMask(currentMask.id)">Редактировать</button>
        </div>
        <button @click="nextMask" :disabled="!hasNextMask">➡️</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      masks: Array,
      selectedMaskIndex: Number,
      currentMask: Object,
      hasMoreMasks: Boolean,
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
    },
  };
  </script>
  
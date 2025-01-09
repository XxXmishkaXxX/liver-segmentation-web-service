<script setup>
import { RouterView } from 'vue-router';
import  HeaderComponent from './components/indexComponents/HeaderComponent.vue'
import FooterComponent from './components/indexComponents/FooterComponent.vue';
</script>

<template>
  <div id="root">
    <HeaderComponent />
      <RouterView />
    <FooterComponent />
  </div>
</template>

<style>
  @import './styles/style.css'
</style>
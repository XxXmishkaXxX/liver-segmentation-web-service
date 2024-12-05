<template>
    <div>
      <h2>{{ formTitle }}</h2>
      <component :is="currentForm" @switch-form="switchForm" />
    </div>
  </template>
  
  <script>
  import { ref, computed } from 'vue';
  import RegistrationComponent from '../components/RegistrationComponent.vue';
  import LoginComponent from '../components/LoginComponent.vue';
  
  export default {
    components: {
      RegistrationComponent,
      LoginComponent,
    },
    setup() {
      const currentForm = ref('RegistrationComponent'); // Используем имя компонента
      const formTitle = computed(() =>
        currentForm.value === 'RegistrationComponent' ? 'Регистрация' : 'Вход'
      );
  
      const switchForm = () => {
        currentForm.value =
          currentForm.value === 'RegistrationComponent'
            ? 'LoginComponent'
            : 'RegistrationComponent';
      };
  
      return {
        currentForm,
        formTitle,
        switchForm,
      };
    },
  };
  </script>
  
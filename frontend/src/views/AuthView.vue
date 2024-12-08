<template>
  <div>
    <component :is="currentForm" @switch-form="switchForm" />
  </div>
</template>

<script>
import { ref } from 'vue';
import RegistrationComponent from '../components/RegistrationComponent.vue';
import LoginComponent from '../components/LoginComponent.vue';

export default {
  components: {
    RegistrationComponent,
    LoginComponent,
  },
  setup() {
    const currentForm = ref('RegistrationComponent'); // Начальная форма - регистрация
    const switchForm = () => {
      currentForm.value =
        currentForm.value === 'RegistrationComponent'
          ? 'LoginComponent'
          : 'RegistrationComponent';
    };


    return {
      currentForm,
      switchForm,
    };
  },
};
</script>

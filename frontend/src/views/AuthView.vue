<template>
  <div>
    <component :is="currentForm" @switch-form="switchForm" />
  </div>
</template>

<script>
import { ref, watch } from 'vue';
import RegistrationComponent from '../components/auth/RegistrationComponent.vue';
import LoginComponent from '../components/auth/LoginComponent.vue';

export default {
  components: {
    RegistrationComponent,
    LoginComponent,
  },
  props: {
    initialForm: {
      type: String,
      required: true, // Ожидается 'login' или 'register'
    },
  },
  setup(props) {
    const currentForm = ref(
      props.initialForm === 'login' ? 'LoginComponent' : 'RegistrationComponent'
    );

    const switchForm = () => {
      currentForm.value =
        currentForm.value === 'RegistrationComponent'
          ? 'LoginComponent'
          : 'RegistrationComponent';
    };

    // Слежение за изменением пути (если маршрут изменился)
    watch(
      () => props.initialForm,
      (newForm) => {
        currentForm.value =
          newForm === 'login' ? 'LoginComponent' : 'RegistrationComponent';
      }
    );

    return {
      currentForm,
      switchForm,
    };
  },
};
</script>

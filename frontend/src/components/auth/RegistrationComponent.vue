<template>
  <div class="container mt-5 text-white">
    <h2>Регистрация</h2>
    
    <!-- Форма регистрации -->
     <div v-if="!isVerification">
      <form @submit.prevent="registerUser">
        <div class="mb-3">
          <label for="firstName" class="form-label">Имя:</label>
          <input type="text" id="firstName" v-model="firstName" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="lastName" class="form-label">Фамилия:</label>
          <input type="text" id="lastName" v-model="lastName" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">Email:</label>
          <input type="email" id="email" v-model="email" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Пароль:</label>
          <input type="password" id="password" v-model="password" class="form-control" required />
        </div>
        <div class="mb-3">
          <button type="submit" class="btn btn-primary">Зарегистрироваться</button>
        </div>
      </form>
      <p>Уже есть аккаунт? <a href="#" @click.prevent="$emit('switch-form')">Войти</a></p>
      </div>
      <!-- Компонент верификации (показывается после успешной регистрации) -->
      <VerificationCodeComponent
        v-if="isVerification"
        :email="email"
        :password="password"
      />
  </div>
</template>

<script>
import VerificationCodeComponent from './VerificationCodeComponent.vue';  // Импортируем компонент верификации
import { toastMixin } from '../../mixins/notifications';

export default {
  components: {
    VerificationCodeComponent
  },
  data() {
    return {
      firstName: '',
      lastName: '',
      email: '',
      password: '',
      isVerification: false,  // Флаг для отображения компонента верификации
    };
  },
  mixins: [toastMixin],
  methods: {
    async registerUser() {
      try {
        const response = await this.$api.post('users/registration/', {
          first_name: this.firstName,
          last_name: this.lastName,
          email: this.email,
          password: this.password,
        });
        console.log(response)
        if (response.data.success) {
          this.showInfoMessage('На почту ' + this.email + ' пришел код для подтверждения почты');
          this.isVerification = true;  // Переходим к компоненту верификации
        } 
      } catch (error) {
        console.log(error.response.data);
        this.showErrorMessage(error.response.data.email);
      }
    },
  }
};
</script>

<style scoped>
.container {
  max-width: 500px;
}
</style>

<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <h2 class="text-center mb-4">Войти</h2>
        <form @submit.prevent="loginUser">
          <div class="mb-3">
            <label for="email" class="form-label">Email:</label>
            <input type="email" id="email" v-model="email" class="form-control" required />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Пароль:</label>
            <input type="password" id="password" v-model="password" class="form-control" required />
          </div>
          <div class="d-grid">
            <button type="submit" class="btn btn-primary">Войти</button>
          </div>
        </form>
        <p class="mt-3 text-center">
          Нет аккаунта? <a href="#" @click.prevent="$emit('switch-form')">Зарегистрироваться</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { toastMixin } from '../mixins/notifications';

export default {
  data() {
    return {
      email: '',
      password: '',
    };
  },
  mixins: [toastMixin],
  methods: {
    async loginUser() {
      try {
        const loginResponse = await this.$api.post('users/token/', {
          email: this.email,
          password: this.password,
        });

        if (loginResponse.data.access) {
          // Сохраняем токен и переходим в рабочую область
          localStorage.setItem('access_token', loginResponse.data.access);
          this.$router.push('/workspace/');
        }
      } catch (error) {
        // Show error message if there is an issue
        this.showErrorMessage(error.response?.data?.email || 'Ошибка авторизации');
      }
    },
  },
};
</script>

<style scoped>
/* Add any additional styles here if needed */
</style>

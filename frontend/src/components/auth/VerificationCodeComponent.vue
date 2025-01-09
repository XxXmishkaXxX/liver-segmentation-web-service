<template>
  <div class="container mt-5">
    <h2>Подтверждение Email</h2>
    <form @submit.prevent="verifyCode">
      <div class="mb-3">
        <label for="code" class="form-label">Код подтверждения:</label>
        <input type="text" id="code" v-model="code" class="form-control" required />
      </div>
      <div class="mb-3">
        <button type="submit" class="btn btn-primary">Подтвердить</button>
      </div>
    </form>
  </div>
</template>

<script>
import { toastMixin } from '../../mixins/notifications';

export default {
  props: ['email', 'password'],  // Принимаем почту и пароль через props
  data() {
    return {
      code: '',  // Код подтверждения, который вводит пользователь
    };
  },
  mixins: [toastMixin],
  methods: {
    async verifyCode() {
      try {
        // Отправляем код для верификации
        const response = await this.$api.post('users/confirm-email/', {
          email: this.email,
          code: this.code,
        });
        
        if (response.data.success) {
          // Если код правильный, пробуем войти в систему
          const loginResponse = await this.$api.post('users/token/', {
            email: this.email,
            password: this.password,  // Используем пароль, переданный через props
          });
          
          if (loginResponse.data.access) {
            // Сохраняем токен и переходим в рабочую область
            localStorage.setItem('access_token', loginResponse.data.access);
            this.$router.push('/workspace/');
          }
        }
      } catch (error) {
        // Выводим ошибку при неправильном коде или истечении времени
        this.showErrorMessage('Неправильный код или срок давности истек');
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 500px;
}
</style>

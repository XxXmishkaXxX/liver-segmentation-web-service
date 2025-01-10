<template>
  <div class="container mt-5 login-box mb-10">
    <h2>Войти</h2>
    <form @submit.prevent="loginUser" class="mb-3">
      <div class="mb-3">
        <input type="email" id="email" v-model="email" placeholder="Почта" class="form-control custom-input" required />
      </div>
      <div class="mb-3">
        <input type="password" id="password" v-model="password" placeholder="Пароль" class="form-control custom-input" required />
      </div>
      <button type="submit" class="submit-button">Войти</button>
    </form>
    <p>Нет аккаунта? <a href="#" @click.prevent="$emit('switch-form')">Зарегистрироваться</a></p>
  </div>
</template>

<script>
import { toastMixin } from '../../mixins/notifications';

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
          localStorage.setItem('access_token', loginResponse.data.access);
          this.$router.push('/workspace/');
        }
      } catch (error) {
        this.showErrorMessage(error.response?.data?.email || 'Ошибка авторизации');
      }
    },
  },
};
</script>

<style scoped>
.login-box {
  max-width: 400px;
  padding: 20px;
  background: #f0f0f0;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  font-weight: bold;
}

.mb-10 {
  margin-bottom: 100px;
}

.custom-input {
  border: none;
  border-bottom: 2px solid #000;
  background: transparent;
  color: #000;
  padding: 10px;
  width: 100%;
  box-shadow: none;
  border-radius: 0px;
}

.custom-input:focus {
  outline: none;
  border-bottom: 2px solid #333;
}

.submit-button {
  width: 100%;
  padding: 10px;
  background: #333;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-button:hover {
  background: #555;
}

p {
  text-align: center;
  font-size: 14px;
}

a {
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>

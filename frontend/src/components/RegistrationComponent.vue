<template>
    <div>
      <form @submit.prevent="registerUser">
        <div>
          <label for="email">Email:</label>
          <input type="email" v-model="email" required />
        </div>
        <div>
          <label for="password">Пароль:</label>
          <input type="password" v-model="password" required />
        </div>
        <div>
          <button type="submit">Зарегистрироваться</button>
        </div>
      </form>
      <p>Уже есть аккаунт? <a href="#" @click.prevent="$emit('switch-form')">Войти</a></p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        email: '',
        password: '',
      };
    },
    methods: {
      async registerUser() {
        try {
          const response = await axios.post('http://your-backend-api.com/register/', {
            email: this.email,
            password: this.password,
          });
          if (response.data.success) {
            this.$router.push('/login');
          } else {
            alert('Ошибка регистрации');
          }
        } catch (error) {
          console.error('Ошибка регистрации:', error);
        }
      },
    },
  };
  </script>
  
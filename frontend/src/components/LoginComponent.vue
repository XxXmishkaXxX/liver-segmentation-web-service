<template>
    <div>
      <form @submit.prevent="loginUser">
        <div>
          <label for="email">Email:</label>
          <input type="email" v-model="email" required />
        </div>
        <div>
          <label for="password">Пароль:</label>
          <input type="password" v-model="password" required />
        </div>
        <div>
          <button type="submit">Войти</button>
        </div>
      </form>
      <p>Нет аккаунта? <a href="#" @click.prevent="$emit('switch-form')">Зарегистрироваться</a></p>
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
      async loginUser() {
        try {
          const response = await axios.post('http://your-backend-api.com/login/', {
            email: this.email,
            password: this.password,
          });
          if (response.data.access_token) {
            localStorage.setItem('access_token', response.data.access_token);
            this.$router.push('/');
          } else {
            alert('Неверные данные для входа');
          }
        } catch (error) {
          console.error('Ошибка входа:', error);
        }
      },
    },
  };
  </script>
  
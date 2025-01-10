<template>
  <div class="container mt-5 registration-box mb-10">
    <h2>Регистрация</h2>

    <div v-if="!isVerification">
      <form @submit.prevent="registerUser" class="mb-3">
        <div class="mb-3">
          <input type="text" id="firstName" v-model="firstName" placeholder="Имя" class="form-control custom-input" required />
        </div>
        <div class="mb-3">
          <input type="text" id="lastName" v-model="lastName" placeholder="Фамилия" class="form-control custom-input" required />
        </div>
        <div class="mb-3">
          <input type="email" id="email" v-model="email" placeholder="Почта" class="form-control custom-input" required />
        </div>
        <div class="mb-3">
          <input type="password" id="password" v-model="password" placeholder="Пароль" class="form-control custom-input" required />
        </div>

        <button type="submit" class="submit-button">Зарегистрироваться</button>
      </form>
      <p>Уже зарегистрированы? <a href="#" @click.prevent="$emit('switch-form')">Войти</a></p>
    </div>

    <VerificationCodeComponent v-if="isVerification" :email="email" :password="password" />
  </div>
</template>

<script>
import VerificationCodeComponent from './VerificationCodeComponent.vue';
import { toastMixin } from '../../mixins/notifications';

export default {
  components: {
    VerificationCodeComponent
  },
  data() {
    return {
      email: '',
      firstName: '',
      lastName: '',
      password: '',
      confirmPassword: '',
      dataConsent: false,
      isVerification: false
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
        if (response.data.success) {
          this.showInfoMessage(`На почту ${this.email} пришел код для подтверждения почты`);
          this.isVerification = true;
        }
      } catch (error) {
        this.showErrorMessage(error.response.data.email);
      }
    }
  }
};
</script>

<style scoped>
.registration-box {
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

.mb-10{
  margin-bottom: 100px;
}

.form-group {
  margin-bottom: 16px;
}

label {
  display: block;
  font-size: 14px;
  margin-bottom: 6px;
}

.form-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
}

.form-checkbox {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.form-checkbox label {
  margin-left: 8px;
  font-size: 14px;
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

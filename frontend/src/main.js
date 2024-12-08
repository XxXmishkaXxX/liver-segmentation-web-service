import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import api from './plugins/axios';

import 'bootstrap/dist/css/bootstrap.css';

import 'bootstrap/dist/js/bootstrap.bundle.js';




const app = createApp(App);

app.use(router);
app.config.globalProperties.$api = api;

app.mount('#app');
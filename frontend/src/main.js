import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import api from './plugins/axios';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.bundle.js';
import '@fortawesome/fontawesome-free/css/all.css';
import 'bootstrap-icons/font/bootstrap-icons.css'; 




const app = createApp(App);

app.use(router);
app.config.globalProperties.$api = api;

app.mount('#app');
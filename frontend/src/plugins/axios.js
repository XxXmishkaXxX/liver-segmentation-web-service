import axios from 'axios';
import { useRouter } from 'vue-router';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.defaults.withCredentials = true;

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Получаем refresh токен из локального хранилища
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        const response = await api.post('users/token/refresh/', { refresh: refreshToken }, { withCredentials: true });

        const newAccessToken = response.data.access;
        localStorage.setItem('access_token', newAccessToken);

        // Повторяем запрос с новым access токеном
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
        return api(originalRequest); // Повторяем запрос с новым токеном
      } catch (refreshError) {
        console.error('Refresh token expired or invalid', refreshError);

        const router = useRouter();
        router.push('/auth/'); // Перенаправляем на страницу авторизации
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;

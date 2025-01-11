const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/images': {
        target: 'http://backend:8000', // URL вашего бэкенда
        changeOrigin: true, // Изменяет заголовок Origin, чтобы соответствовать целевому серверу
      },
    },
  },
});

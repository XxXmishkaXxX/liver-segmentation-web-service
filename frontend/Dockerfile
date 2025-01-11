# Dockerfile для Vue.js Frontend
FROM node:18

# Установка рабочей директории
WORKDIR /app

# Копирование package.json и package-lock.json
COPY package*.json ./

# Установка зависимостей
RUN npm install

# Копирование остальных файлов проекта
COPY . .

# Сборка проекта
RUN npm run build

# Запуск приложения
CMD ["npm", "run", "serve"]

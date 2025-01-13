FROM python:3.11

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libsm6 libxext6 libxrender-dev && \
    rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY . /app

RUN pip cache purge

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Установка переменной окружения для Django
ENV PYTHONUNBUFFERED 1

# Команда запуска (может быть изменена в зависимости от среды)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

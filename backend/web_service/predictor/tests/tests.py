from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from predictor.models import ModelPredictionBatch, Image
import os
from django.conf import settings
import pydicom
from django.core.files.base import ContentFile
from celery.result import AsyncResult
import time
from django.db import transaction



# class ImageUploadTestCase(APITestCase):
#     def setUp(self):
#         # Создаем пользователя для теста
#         self.user = User.objects.create_user(email="testuser@mail.ru", password="testpassword")
#         self.user.is_active = True  # Активируем пользователя
#         self.user.save()
        
#         # Создаем JWT токен для аутентификации
#         refresh = RefreshToken.for_user(self.user)
#         self.token = str(refresh.access_token)
        
#         self.image_folder = os.path.join(settings.BASE_DIR, 'predictor', 'tests', 'imgs', '3', 'DICOM_anon')

#         # Получаем список всех файлов в папке, которые могут быть изображениями
#         self.dicom_files = [
#             os.path.join(self.image_folder, f) for f in os.listdir(self.image_folder)
#             if f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'dcm'))
#         ]

#     def test_upload_images_from_folder(self):
#         files = []
    
#         # Перебираем все файлы в папке и готовим их для загрузки
#         for dicom_file_path in self.dicom_files:
#             print(dicom_file_path)
#             with open(dicom_file_path, 'rb') as f:
#                 dicom_content = f.read()
#                 file_name = os.path.basename(dicom_file_path)
#                 files.append(SimpleUploadedFile(file_name, dicom_content))
        
#         url = '/api/upload/'  # Адрес вашего API для загрузки изображений
#         headers = {'Authorization': f'Bearer {self.token}'}
#         print(headers)
        
#         # Отправляем запрос с изображениями из папки
#         response = self.client.post(url, {'files': files}, format='multipart', HTTP_AUTHORIZATION='Bearer {0}'.format(self.token))
        
#         # Проверяем, что ответ имеет код 201
#         # self.assertEqual(response.status_code, 201)
            
#         # Проверяем, что был создан батч
#         batch_data = response.data
#         batch_id = batch_data['id']
#         batch = ModelPredictionBatch.objects.get(id=batch_id)
        
#         # Проверяем, что количество изображений в батче соответствует количеству загруженных файлов
#         self.assertEqual(batch.image_count, len(self.dicom_files))
        
#         # Проверяем, что все изображения сохранены
#         images = batch.images.all()
#         self.assertEqual(images.count(), len(self.dicom_files))
        
#         # Проверяем, что файлы существуют
#         for image in images:
#             self.assertTrue(os.path.exists(image.image_file.path))
#             self.assertEqual(image.image_type, 'origin')  # Проверяем, что тип изображения - 'origin'

#     def test_invalid_file_type(self):
#         # Загружаем не DICOM файл
#         invalid_file = SimpleUploadedFile("test.txt", b'Invalid file content', content_type="text/plain")
#         url = '/api/upload/'
#         data = {'files': invalid_file}
#         headers = {'Authorization': f'Bearer {self.token}'}
        
#         # Отправляем запрос
#         response = self.client.post(url, data, format='multipart', headers=headers)
        
#         # Проверяем, что ответ содержит ошибку с неподдерживаемым типом файла
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("Unsupported file type", response.data["error"])



class BatchPredictTestCase(APITestCase):
    
    def setUp(self):
        # Создаем пользователя для теста
        self.user = User.objects.create_user(email="testuser@mail.ru", password="testpassword")
        self.user.is_active = True  # Активируем пользователя
        self.user.save()
        
        # Создаем JWT токен для аутентификации
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        
        self.image_folder = os.path.join(settings.BASE_DIR, 'predictor', 'tests', 'imgs', '3', 'DICOM_anon')

        # Получаем список всех файлов в папке, которые могут быть изображениями
        self.dicom_files = [
            os.path.join(self.image_folder, f) for f in os.listdir(self.image_folder)
            if f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'dcm'))
        ]

        self.batch = ModelPredictionBatch.objects.create(user=self.user,           
                                                    image_count=0)

        print(self.batch)
        # Создаем изображения и добавляем их в батч
        self.uploaded_images = []
        for dicom_file_path in self.dicom_files:
            # Читаем DICOM файл с помощью pydicom
            dicom_data = pydicom.dcmread(dicom_file_path)

            # Сохраняем DICOM файл как есть, без изменений
            dicom_bytes = self.get_dicom_bytes(dicom_data)

            dicom_file_name = os.path.basename(dicom_file_path)
            dicom_content = ContentFile(dicom_bytes, name=dicom_file_name)
    
            Image.objects.create(user=self.user, batch=self.batch, image_file=dicom_content)

            
            

    def get_dicom_bytes(self, dicom_data):
        """
        Преобразует DICOM объект в байтовое представление для хранения в базе данных.
        """
        dicom_bytes = BytesIO()
        dicom_data.save_as(dicom_bytes)
        dicom_bytes.seek(0)  # Возвращаемся в начало байтового потока
        return dicom_bytes.getvalue()

    def test_batch_predict(self):
        # Отправляем запрос на предсказание для этого батча
        url = f'/api/batch/{self.batch.id}/predict/'  # Путь к API для предсказания
        response = self.client.get(url, HTTP_AUTHORIZATION='Bearer {0}'.format(self.token))

        print(response.json())
        task_id = response.data['task_id']
        result = AsyncResult(task_id)

        # Проверяем, что запрос прошел успешно
        # self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        while not result.ready():
            print(result)
            time.sleep(1)

        # Получаем результат задачи
        predictions = result.result
        print(predictions)
        # Проверяем, что предсказания были выполнены
        # self.assertIsNotNone(predictions)
        # self.assertEqual(len(predictions), len(self.dicom_files))
        # Получаем обновленный батч и проверяем его статус
        self.batch.refresh_from_db()
        # self.assertEqual(self.batch.status, 'completed')  # Ожидаем, что статус будет "completed"


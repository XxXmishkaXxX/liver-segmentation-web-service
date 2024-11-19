import os
from django.db import models
from users.models import User


class ModelPredictionBatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prediction_batches')
    created_at = models.DateTimeField(auto_now_add=True)
    image_count = models.PositiveIntegerField()

    def __str__(self):
        return f"Batch {self.id} - User: {self.user.username} - {self.image_count} images"

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    batch = models.ForeignKey(ModelPredictionBatch, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to='images/')  # Путь для сохранения
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)  # Обработано ли изображение моделью
    image_type = models.CharField(max_length=10, choices=[('origin', 'Original'), ('mask', 'Mask')], default='origin')

    def __str__(self):
        return f"Image {self.id} - Batch {self.batch.id} - User: {self.user.username} - Type: {self.image_type}"

    def save(self, *args, **kwargs):
        # Определяем путь сохранения в зависимости от типа изображения
        image_count = self.batch.images.count() + 1  # Увеличиваем счетчик на 1
        file_extension = os.path.splitext(self.image_file.name)[1]  # Получаем расширение файла

        if self.image_type == 'origin':
            # Для исходных изображений сохраняем в origin
            self.image_file.name = f'images/{self.user.id}/{self.batch.id}/origin/image{image_count}{file_extension}'
        elif self.image_type == 'mask':
            # Для масок сохраняем в masks
            self.image_file.name = f'images/{self.user.id}/{self.batch.id}/masks/image{image_count}{file_extension}'

        super().save(*args, **kwargs)

import os
from django.db import models
from users.models import User
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.base import ContentFile
import os

class ModelPredictionBatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prediction_batches')
    created_at = models.DateTimeField(auto_now_add=True)
    image_count = models.PositiveIntegerField()

    def __str__(self):
        return f"Batch {self.id} - User: {self.user.email} - {self.image_count} images"

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    batch = models.ForeignKey(ModelPredictionBatch, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to='images/')  # Путь для сохранения
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)  # Обработано ли изображение моделью

    def __str__(self):
        return f"Image {self.id} - Batch {self.batch.id} - User: {self.user.email}"

    def save(self, *args, **kwargs):
        file_name = self.image_file.name.split('/')[-1]
        self.image_file.name = f'{self.user.id}/batch_{self.batch.id}id/origin/{file_name}'
        
        super().save(*args, **kwargs)


class MaskImage(models.Model):
    original_img = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='original_image')
    image_file = models.ImageField(upload_to='images/')  # Путь для маски
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Mask {self.id} - Image ID: {self.original_img.id}"
    
    def save(self, *args, **kwargs):
        file_name = self.image_file.name.split('/')[-1]
        self.image_file.name = f"{self.original_img.user.id}/batch_{self.original_img.batch.id}id/masks/{file_name}"
        super().save(*args, **kwargs)
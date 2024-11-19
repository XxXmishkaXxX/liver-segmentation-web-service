from rest_framework import serializers
from .models import ModelPredictionBatch, Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'user', 'batch', 'image_file', 'created_at', 'processed', 'image_type']

class ModelPredictionBatchSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)  # Включаем связанные изображения

    class Meta:
        model = ModelPredictionBatch
        fields = ['id', 'user', 'created_at', 'image_count', 'images']
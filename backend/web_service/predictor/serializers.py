from rest_framework import serializers
from .models import ModelPredictionBatch, Image, MaskImage

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'user', 'batch', 'image_file', 'created_at', 'processed',]


class MaskImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaskImage
        fields = ['id', 'image_file']

class ModelPredictionBatchSerializer(serializers.ModelSerializer):
    first_img = serializers.SerializerMethodField()

    class Meta:
        model = ModelPredictionBatch
        fields = ['id', 'user', 'created_at', 'image_count', 'first_img']

    def get_first_img(self, obj):
    # Получаем первое изображение из батча
        first_image = obj.images.first()
        if first_image and first_image.image_file_png:
            # Проверяем, есть ли файл в поле image_file_png
            return {'image_url': first_image.image_file_png.url}
        return None
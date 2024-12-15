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
    first_mask = serializers.SerializerMethodField()

    class Meta:
        model = ModelPredictionBatch
        fields = ['id', 'user', 'created_at', 'image_count', 'first_mask']

    def get_first_mask(self, obj):
        # Получаем первое изображение из батча
        first_image = obj.images.first()  # 'images' — это имя обратной связи для связи с Image
        if first_image:
            # Находим первую маску для этого изображения
            first_mask = first_image.original_image.first()  # 'original_image' — связь с MaskImage
            if first_mask:
                return MaskImageSerializer(first_mask).data
        return None
from rest_framework import serializers
from .models import ModelPredictionBatch, Image, MaskImage

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'user', 'batch', 'image_file', 'created_at', 'processed',]


class MaskImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = MaskImage
        fields = ['id',]

class ModelPredictionBatchSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = ModelPredictionBatch
        fields = ['id', 'user', 'created_at', 'image_count', 'first_image']

    def get_first_image(self, obj):
        # Предполагается, что у ModelPredictionBatch есть связь с Image через Related Manager, например, `images`
        first_image = obj.images.first()  # images — это имя обратной связи
        if first_image:
            return ImageSerializer(first_image).data
        return None
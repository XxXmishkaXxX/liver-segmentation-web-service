from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import ModelPredictionBatch, Image
from .serializers import ModelPredictionBatchSerializer
from django.shortcuts import get_object_or_404
from .serializers import ImageSerializer

class UploadImagesView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        uploaded_files = request.FILES.getlist('files')

        if not uploaded_files:
            return Response({"error": "No files uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        batch = ModelPredictionBatch.objects.create(user=request.user, image_count=0)

        for file in uploaded_files:
            if file.name.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'dcm')):
                Image.objects.create(
                    user=request.user,
                    batch=batch,
                    image_file=file,
                    image_type='origin'
                )
            else:
                return Response({"error": f"Unsupported file type: {file.name}"}, status=status.HTTP_400_BAD_REQUEST)

        # Обновляем счетчик изображений
        batch.image_count = batch.images.count()
        batch.save()

        serializer = ModelPredictionBatchSerializer(batch)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class BatchPredictionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, batch_id, *args, **kwargs):
        batch = get_object_or_404(ModelPredictionBatch, id=batch_id, user=request.user)
        images = batch.images.filter(image_type='origin', processed=False)

        if not images.exists():
            return Response({"error": "No unprocessed images found in this batch"}, status=status.HTTP_400_BAD_REQUEST)

        for image in images:
            # Пример работы модели: создаем маску
            # mask = run_prediction_on_image(image.image_file.path)
            
            # Сохраняем маску как новое изображение
            Image.objects.create(
                user=request.user,
                batch=batch,
                image_file=image.image_file.name.replace('origin', 'mask'),
                image_type='mask',
                processed=True
            )

            # Отмечаем оригинальное изображение как обработанное
            image.processed = True
            image.save()

        processed_images = batch.images.filter(image_type='mask')
        serializer = ImageSerializer(processed_images, many=True)

        return Response({"batch_id": batch.id, "predicted_images": serializer.data}, status=status.HTTP_200_OK)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import ModelPredictionBatch, Image, MaskImage
from .serializers import ModelPredictionBatchSerializer
from django.shortcuts import get_object_or_404
from .tasks import process_images_in_batch
from rest_framework import pagination


class UploadImagesView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        uploaded_files = request.FILES.getlist('files')
        print(request.FILES)
        if not uploaded_files:
            return Response({"error": "No files uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        batch = ModelPredictionBatch.objects.create(user=request.user, image_count=0)

        # Поддерживаемые форматы
        supported_formats = {'jpg', 'jpeg', 'png', 'bmp', 'dcm'}
        
        for file in uploaded_files:
            file_extension = file.name.lower().split('.')[-1]
            if file_extension in supported_formats:
                Image.objects.create(
                    user=request.user,
                    batch=batch,
                    image_file=file,
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

        # Проверяем, есть ли необработанные изображения
        images = batch.images.filter(processed=False)

        if not images.exists():
            return Response({"error": "No unprocessed images found in this batch"}, status=status.HTTP_400_BAD_REQUEST)

        # Отправляем задачу Celery для асинхронной обработки изображений
        result = process_images_in_batch.delay(batch_id, request.user.id)

        # Возвращаем ответ о том, что задача запущена
        return Response({
            "batch_id": batch.id,
            "message": "Batch processing started",
            "task_id": result.id  # Добавляем task_id в ответ
        }, status=status.HTTP_202_ACCEPTED)
    


class DeleteBatchView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, batch_id, *args, **kwargs):
        # Получаем батч или возвращаем ошибку, если его нет
        batch = get_object_or_404(ModelPredictionBatch, id=batch_id, user=request.user)

        # Удаляем все фотографии в батче
        batch.images.all().delete()

        # Удаляем сам батч
        batch.delete()

        return Response({"message": "Batch and all images successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


class ImagePagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

class GetBatchImagesView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ImagePagination

    def get(self, request, batch_id, *args, **kwargs):
        # Получаем все изображения из данного пакета
        images = Image.objects.filter(user=request.user, batch_id=batch_id)
        masks = MaskImage.objects.filter(original_img__in=images)


        # Формируем словарь масок с использованием имени оригинала без _mask
        mask_dict = {
            mask.original_img.image_file.name.split('/')[-1].split('.')[0].replace('_mask', ''): mask
            for mask in masks
        }

        # Формируем список пар (оригинал + маска)
        image_pairs = []
        for original in images:
            original_name = original.image_file.name.split('/')[-1].split('.')[0]  # Получаем имя файла без пути и расширения
            mask = mask_dict.get(original_name)  # Ищем маску по имени оригинала

            if mask:
                image_pairs.append({
                    'original': original.image_file.url,
                    'mask': mask.image_file.url
                })
        
        # Пагинация
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(image_pairs, request)
        return paginator.get_paginated_response(result_page)
    




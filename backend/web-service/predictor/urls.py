from django.urls import path
from .views import UploadImagesView, BatchPredictionView

urlpatterns = [
    path('upload/', UploadImagesView.as_view(), name='upload-images'),
    path('batch/<int:batch_id>/predict/', BatchPredictionView.as_view(), name='batch-predict'),
]
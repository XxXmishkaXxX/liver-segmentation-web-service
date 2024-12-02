from django.urls import path
from .views import UploadImagesView, BatchPredictionView, DeleteBatchView, GetBatchImagesView

urlpatterns = [
    path('upload/', UploadImagesView.as_view(), name='upload-images'),
    path('batch/<int:batch_id>/predict/', BatchPredictionView.as_view(), name='batch-predict'),
    path('delete_batch/<int:batch_id>/', DeleteBatchView.as_view(), name='delete_batch'),
    path('batch/<int:batch_id>/images/', GetBatchImagesView.as_view(), name='get_batch_images'),

]
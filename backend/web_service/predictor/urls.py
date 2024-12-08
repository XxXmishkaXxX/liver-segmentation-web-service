from django.urls import path
from .views import (TaskStatusView,
                    UploadImagesView, 
                    BatchPredictionView, 
                    DeleteBatchView, 
                    GetBatchImagesView, 
                    UpdateMaskImage,
                    GetAllBatchesUser)

urlpatterns = [
    path('task-status/<str:task_id>/', TaskStatusView.as_view(), name='task_status'),
    path('upload/', UploadImagesView.as_view(), name='upload-images'),
    path('batch/<int:batch_id>/predict/', BatchPredictionView.as_view(), name='batch-predict'),
    path('delete-batch/<int:batch_id>/', DeleteBatchView.as_view(), name='delete_batch'),
    path('batch/<int:batch_id>/images/', GetBatchImagesView.as_view(), name='get_batch_images'),
    path('update-mask/<int:mask_id>/', UpdateMaskImage.as_view(), name='update_mask'),
    path('batches/', GetAllBatchesUser.as_view(), name='all-user-bacthes')
]
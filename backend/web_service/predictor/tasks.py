import os
from celery import shared_task # type: ignore
from typing import List
from .models import ModelPredictionBatch, MaskImage
from .utils.prediction import run_prediction_on_image
from .utils.change_mask_color import make_yellow_mask_with_transparency

import logging
logger = logging.getLogger(__name__)


@shared_task
def process_images_in_batch(batch_id: int, user_email: str):
    logger.info(f"Starting batch processing for batch ID {batch_id}")
    try:
        batch = ModelPredictionBatch.objects.get(id=batch_id, user=user_email)
    except ModelPredictionBatch.DoesNotExist:
        return f"Batch with ID {batch_id} does not exist."

    images = batch.images.all()
    
    for img in images:
        try:
            img_name = img.image_file.name.split('/')[-1].split('.')[0]
            
            mask = run_prediction_on_image(img.image_file.path)  # Функция предсказания

            image_with_mask = make_yellow_mask_with_transparency(mask, img_name)

            mask_image = MaskImage.objects.create(
                original_img=img,
                image_file=image_with_mask,
            )

            img.processed = True
            img.save()

        except Exception as e:
            print(f"Error processing image {img.id}: {str(e)}")  # Принт ошибки, если возникает исключение

    if not batch.images.filter(processed=False).exists():
        batch.status = 'completed'
        batch.save()
        print(f"Batch {batch_id} processing completed.")  # Принт, когда батч завершен

    return f"Batch {batch_id} processing completed."




from django.core.files.base import ContentFile
import os

def update_mask(mask, new_mask):

    old_file_path = mask.image_file.path

    new_mask_content = new_mask.read()
    new_mask = ContentFile(new_mask_content, name=mask.image_file.name)

    mask.image_file = new_mask  # Заменяем старое изображение на новое
    
    if os.path.exists(old_file_path):
        os.remove(old_file_path)

    # Сохраняем маску в базе данных
    mask.save()

    return
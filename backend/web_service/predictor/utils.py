import numpy as np
import tensorflow as tf
from keras.models import load_model
import os
from pydicom import dcmread
import cv2
from .model.custom_objects import dice_coef, dice_coef_loss
from django.core.files.base import ContentFile

# Загрузка модели

model_path = os.path.join(os.path.dirname(__file__), 'model', 'best_model.keras')
 
model = load_model(model_path, custom_objects={'dice_coef': dice_coef, 'dice_coef_loss': dice_coef_loss})

def run_prediction_on_image(image_path: str, image_size=(128, 128)):
    image = dcmread(image_path)
    image = image.pixel_array
    image = cv2.resize(image, image_size)  # Ресайз на 128x128
    image = np.expand_dims(image, axis=-1)  # Добавляем размерность канала (1, 128, 128, 1)
    image = image / 255.0  # Нормализация изображения

    image = np.expand_dims(image, axis=0)  # Добавляем batch dimension (1, 128, 128, 1)
    
    # Предсказание маски моделью
    predicted_mask = model.predict(image)[0]
    

    return image, predicted_mask

# Функция для наложения маски на изображение
def overlay_mask_on_image(image, mask, img_name, alpha=0.5):
    """
    Накладывает маску на изображение с прозрачностью (alpha).
    """

    image = image.squeeze(axis=0)  # Удаляем batch dimension (1, 128, 128, 1) -> (128, 128, 1)
    image = np.repeat(image, 3, axis=-1)  # Делаем 3 канала (128, 128, 3)
    image = (image * 255).astype(np.uint8) # Приводим изображение к формату uint8

    # Маска будет серого цвета и преобразуем в формат (128, 128, 3)
    if mask.ndim == 3 and mask.shape[-1] == 1:  # Если маска одноцветная (128, 128, 1)
        mask_colored = np.repeat(mask, 3, axis=-1)  # Делаем 3 канала (128, 128, 3)
    else:
        mask_colored = mask  # Если маска уже RGB, используем как есть

    mask_colored = (mask_colored * 255).astype(np.uint8)  # Преобразуем маску в цветной формат (0-255)

    # Совмещение изображения и маски
    overlayed_image = cv2.addWeighted(image, 1 - alpha, mask_colored, alpha, 0)

    _, buffer = cv2.imencode('.png', overlayed_image)

    # Преобразуем байтовый массив в ContentFile
    image_content = ContentFile(buffer.tobytes(), name=f"{img_name}_mask.png")
    print(image_content.name)
    return image_content

import numpy as np
from keras.models import load_model #type: ignore
import os
from pydicom import dcmread #type: ignore
import cv2 #type: ignore
from ..model.custom_objects import dice_coef, dice_coef_loss

# Загрузка модели

model_path = os.path.join('predictor', 'model', 'best_model.keras')
 
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


    return predicted_mask


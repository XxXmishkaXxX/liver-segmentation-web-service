import io
import cv2
import numpy as np
import pydicom

# Функция для обработки DICOM файла и предсказания маски
def load_and_predict_dicom_image(dicom_file: bytes, model, image_size=(128, 128)):
    dicom_data = pydicom.dcmread(io.BytesIO(dicom_file))  # Чтение DICOM изображения из байт
    image = dicom_data.pixel_array
    image = cv2.resize(image, image_size)  # Ресайз изображения до 128x128
    image = np.expand_dims(image, axis=-1)  # Добавляем размерность канала
    image = image / 255.0  # Нормализация изображения
    image = np.expand_dims(image, axis=0)  # Добавляем batch размерность
    
    # Предсказание маски моделью
    predicted_mask = model.predict(image)[0]
    
    # Восстановление оригинального размера изображения
    image_original = cv2.resize(image.squeeze(), (512, 512))
    predicted_mask_original = cv2.resize(predicted_mask, (512, 512), interpolation=cv2.INTER_NEAREST)
    
    return image_original, predicted_mask_original


def overlay_mask_on_image(image, mask, alpha=0.5):
    """
    Накладывает полупрозрачную красную маску на изображение.
    """
    # Если изображение одноцветное (1 канал), добавляем 2 дополнительные размерности для RGB
    if image.ndim == 2:  # Если изображение 2D
        image = np.repeat(image[:, :, np.newaxis], 3, axis=-1)  # Делаем 3 канала для RGB

    image = (image * 255).astype(np.uint8)  # Преобразуем изображение в формат uint8

    # Преобразуем маску в цвет (красный канал)
    mask_colored = np.zeros_like(image)
    mask_colored[..., 0] = 255  # Красный канал (R)

    # Умножаем маску на альфа-канал, чтобы сделать её полупрозрачной
    mask_alpha = (mask * 255).astype(np.uint8)  # Маска, умноженная на 255
    mask_colored = cv2.merge([mask_alpha, mask_colored[..., 1], mask_colored[..., 2]])  # Полупрозрачный красный

    # Накладываем маску на изображение с прозрачностью
    overlayed_image = cv2.addWeighted(image, 1 - alpha, mask_colored, alpha, 0)

    return overlayed_image

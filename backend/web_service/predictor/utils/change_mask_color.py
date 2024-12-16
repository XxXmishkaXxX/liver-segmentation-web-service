import numpy as np
import cv2  # type: ignore
from django.core.files.base import ContentFile

def make_yellow_mask_with_transparency(mask, img_name):
    """
    Преобразует маску в изображение с прозрачным фоном и жёлтой маской.
    """
    # Убедимся, что маска в формате (128, 128, 1)
    if mask.ndim == 3 and mask.shape[-1] == 1:
        mask = mask.squeeze(axis=-1)  # Удаляем последнюю размерность

    # Масштабируем значения маски (0-1) в диапазон (0-255)
    mask = (mask * 255).astype(np.uint8)

    # Создаём RGBA изображение
    rgba_mask = np.zeros((mask.shape[0], mask.shape[1], 4), dtype=np.uint8)
    
    # Добавляем жёлтый цвет в маске (RGB: 255, 255, 0)
    rgba_mask[..., 1] = mask  # Красный канал
    rgba_mask[..., 1] = mask  # Зелёный канал
    rgba_mask[..., 2] = 0     # Синий канал

    # Устанавливаем альфа-канал (прозрачность): только область маски остаётся видимой
    rgba_mask[..., 3] = mask  # Прозрачность = значения маски (0 для фона, 255 для маски)

    # Кодируем изображение с прозрачным фоном в PNG формат
    _, buffer = cv2.imencode('.png', rgba_mask)

    # Преобразуем байтовый массив в ContentFile
    mask_content = ContentFile(buffer.tobytes(), name=f"{img_name}_yellow_mask.png")
    print(mask_content.name)
    return mask_content

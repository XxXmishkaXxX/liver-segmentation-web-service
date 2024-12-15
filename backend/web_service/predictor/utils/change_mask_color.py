import numpy as np
import cv2  # type: ignore
from django.core.files.base import ContentFile

def make_yellow_mask(mask, img_name):
    """
    Преобразует маску в жёлтый цвет и сохраняет как отдельное изображение.
    """
    # Убедимся, что маска в формате (128, 128, 1)
    if mask.ndim == 3 and mask.shape[-1] == 1:
        mask = mask.squeeze(axis=-1)  # Удаляем последнюю размерность

    # Масштабируем значения маски (0-1) в диапазон (0-255)
    mask = (mask * 255).astype(np.uint8)

    # Создаём жёлтую маску (RGB: 255, 255, 0)
    yellow_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
    yellow_mask[..., 1] = mask  # Красный канал
    yellow_mask[..., 1] = mask  # Зелёный канал
    # Синий канал остаётся нулевым (жёлтый = красный + зелёный)

    # Кодируем жёлтую маску в PNG формат
    _, buffer = cv2.imencode('.png', yellow_mask)

    # Преобразуем байтовый массив в ContentFile
    mask_content = ContentFile(buffer.tobytes(), name=f"{img_name}_yellow_mask.png")
    print(mask_content.name)
    return mask_content

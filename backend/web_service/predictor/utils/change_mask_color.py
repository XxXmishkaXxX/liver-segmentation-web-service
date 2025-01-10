import numpy as np
import cv2
from django.core.files.base import ContentFile

def make_yellow_mask_with_transparency(mask, img_name):
    """
    Преобразует маску в изображение с прозрачным фоном и жёлтым контуром.
    """
    # Убедимся, что маска в формате (128, 128, 1)
    if mask.ndim == 3 and mask.shape[-1] == 1:
        mask = mask.squeeze(axis=-1)  # Удаляем последнюю размерность

    # Масштабируем значения маски (0-1) в диапазон (0-255)
    mask = (mask * 255).astype(np.uint8)

    # Применяем операцию нахождения контуров
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Создаём пустое изображение для контуров
    contour_image = np.zeros_like(mask)

    # Отображаем контуры на пустом изображении
    cv2.drawContours(contour_image, contours, -1, (255), thickness=1)

    # Создаём RGBA изображение
    rgba_mask = np.zeros((contour_image.shape[0], contour_image.shape[1], 4), dtype=np.uint8)

    # Добавляем жёлтый цвет в маске (RGB: 255, 255, 0)
    rgba_mask[..., 1] = contour_image  # Красный канал
    rgba_mask[..., 1] = contour_image  # Зелёный канал
    rgba_mask[..., 2] = 0             # Синий канал

    # Устанавливаем альфа-канал (прозрачность): только контур остаётся видимым
    rgba_mask[..., 3] = contour_image  # Прозрачность = значения маски (0 для фона, 255 для контуров)

    # Кодируем изображение с прозрачным фоном в PNG формат
    _, buffer = cv2.imencode('.png', rgba_mask)

    # Преобразуем байтовый массив в ContentFile
    mask_content = ContentFile(buffer.tobytes(), name=f"{img_name}_yellow_mask.png")
    return mask_content

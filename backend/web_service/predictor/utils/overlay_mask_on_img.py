import numpy as np
import cv2 #type: ignore
from django.core.files.base import ContentFile



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
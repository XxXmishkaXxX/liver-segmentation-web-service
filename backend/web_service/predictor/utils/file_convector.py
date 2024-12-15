from io import BytesIO
from django.core.files.base import ContentFile
from pydicom import dcmread
from pydicom.multival import MultiValue
import numpy as np
from PIL import Image as PilImage


def convert_dcm_to_png(dcm_file):
    """
    Конвертирует DICOM-файл в PNG.

    :param dcm_file: Файл DICOM (Django File объект).
    :return: Кортеж (имя файла PNG, ContentFile объекта PNG).
    """
    # Чтение DICOM из файла
    dicom = dcmread(dcm_file)

    # Получение массива пикселей
    image_data = dicom.pixel_array.astype(np.float32)

    # Применение RescaleSlope и RescaleIntercept (если есть)
    if hasattr(dicom, "RescaleSlope") and hasattr(dicom, "RescaleIntercept"):
        image_data = image_data * dicom.RescaleSlope + dicom.RescaleIntercept

    # Определение Window Center (WC) и Window Width (WW)
    window_center = getattr(dicom, "WindowCenter", None)
    window_width = getattr(dicom, "WindowWidth", None)

    if isinstance(window_center, MultiValue):
        window_center = window_center[0]  # Если WC — список, берем первый элемент
    if isinstance(window_width, MultiValue):
        window_width = window_width[0]  # Если WW — список, берем первый элемент

    if window_center is not None and window_width is not None:
        # Применение оконного преобразования
        lower_bound = window_center - (window_width / 2)
        upper_bound = window_center + (window_width / 2)
        image_data = np.clip(image_data, lower_bound, upper_bound)

    # Нормализация в диапазон [0, 255]
    image_data -= image_data.min()
    image_data /= image_data.max()
    image_data *= 255.0
    image_data = image_data.astype(np.uint8)

    # Конвертируем в Pillow Image
    pil_image = PilImage.fromarray(image_data)

    # Преобразуем в байтовый поток
    buffer = BytesIO()
    pil_image.save(buffer, format="PNG")
    buffer.seek(0)

    # Создаём ContentFile для сохранения в ImageField
    file_name = dcm_file.name.split('/')[-1].replace('.dcm', '.png')
    return file_name, ContentFile(buffer.read())

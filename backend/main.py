from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO
import os
from backend.model import load_model_unet
from backend.predictor import load_and_predict_dicom_image, overlay_mask_on_image
from PIL import Image



app = FastAPI()

# Загрузка модели при старте приложения
model = load_model_unet()

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Сохраняем временно загруженный файл
    temp_file_path = "temp_dicom.dcm"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(await file.read())

    # Загрузка содержимого файла в память (в байтах)
    with open(temp_file_path, "rb") as f:
        dicom_bytes = f.read()

    # Загружаем и предсказываем изображение
    image, predicted_mask = load_and_predict_dicom_image(dicom_bytes, model)

    # Накладываем маску на изображение
    overlayed_image = overlay_mask_on_image(image, predicted_mask)

    # Сохраняем изображение с маской в буфер
    output_image = BytesIO()
    overlayed_image_pil = Image.fromarray(overlayed_image)
    overlayed_image_pil.save(output_image, format="PNG")
    output_image.seek(0)

    # Возвращаем изображение с маской как PNG
    return StreamingResponse(output_image, media_type="image/png")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

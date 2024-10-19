from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.main import app

client = TestClient(app)


def test_predict():
    with open(r"D:\projects\liver-segmentation-web-service\backend\test_api\test_imgs\IMG-0005-00074.dcm", "rb") as f:
        response = client.post("/predict/", files={"file": f})

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    
    # Проверяем, что возвращаемый файл не пустой
    assert len(response.content) > 0

    # Сохраняем предсказанную картинку для дальнейшего анализа
    with open("predicted_overlayed_image2.png", "wb") as f:
        f.write(response.content)

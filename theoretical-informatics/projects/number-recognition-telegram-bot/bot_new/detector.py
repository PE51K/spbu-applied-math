import torch
from PIL import Image
from config import MODEL_PATH

model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH, force_reload=True)

def detect_image(image_path):

    image = Image.open(image_path)
    results = model(image, size=640)
    print(results)
    results.save()  # Сохраняет обработанное изображение
    return results.files[0]  # Возвращает путь к обработанному изображению

# -*- coding: utf-8 -*-
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
import cv2
import numpy as np
from PIL import Image
import io
import psycopg2  # До этого использовала (скриншот прикреплю по работе с БД)
from psycopg2 import sql  # БД

app = FastAPI()

# Реализация Singleton для FaceCascade
class FaceCascadeSingleton:
    _instance = None

    def __new__(cls, cascade_file):
        if cls._instance is None:
            print("Loading Face Cascade...") # Добавляем print, чтобы видеть запуск
            cls._instance = super(FaceCascadeSingleton, cls).__new__(cls) # Загружаем классификатор Haar Cascade только при создании первого экземпляра
            cls._instance.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascade_file)
        return cls._instance

    def detectMultiScale(self, image, scaleFactor, minNeighbors, minSize=None):
        return self.face_cascade.detectMultiScale(image, scaleFactor, minNeighbors, minSize)


# Получаем экземпляр Singleton для FaceCascade
face_cascade = FaceCascadeSingleton('haarcascade_frontalface_default.xml')

def detect_faces(image_bytes):
    try:
        # Открываем изображение с помощью Pillow
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_array = np.array(img)

        # Преобразуем изображение в оттенки серого
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

        # Обнаруживаем лица на изображении
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Рисуем прямоугольники на изображении
        for (x, y, w, h) in faces:
            cv2.rectangle(img_array, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Зеленый цвет

        # Преобразуем изображение обратно в формат PIL
        img_pil = Image.fromarray(img_array)

        # Создаем объект BytesIO для хранения изображения в памяти
        output_stream = io.BytesIO()

        # Сохраняем изображение в формате JPEG в BytesIO
        img_pil.save(output_stream, format='JPEG')

        # Получаем байтовую строку изображения
        image_bytes = output_stream.getvalue()

        return image_bytes

    except Exception as e:
        print(f"Error detecting faces: {e}")
        return None

@app.post("/detect_faces")
async def detect_faces_endpoint(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        processed_image_bytes = detect_faces(contents)

        if processed_image_bytes:
            return StreamingResponse(io.BytesIO(processed_image_bytes), media_type="image/jpeg")
        else:
            return JSONResponse(content={"message": "Error detecting faces"}, status_code=500)

    except Exception as e:
        print(f"Error processing image: {e}")
        return JSONResponse(content={"message": "Internal server error"}, status_code=500)
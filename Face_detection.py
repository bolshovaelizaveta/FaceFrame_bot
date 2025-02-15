# -*- coding: utf-8 -*-
import io
import os
import numpy as np
from PIL import Image
import cv2

# Получаем экземпляр Singleton для FaceCascade
class FaceCascadeSingleton:
    _instance = None

    def __new__(cls, cascade_file):
        if cls._instance is None:
            print("Loading Face Cascade...")
            cls._instance = super(FaceCascadeSingleton, cls).__new__(cls)
            cls._instance.face_cascade = cv2.CascadeClassifier(cascade_file) 
        return cls._instance

    def detectMultiScale(self, image, scaleFactor, minNeighbors, minSize=None):
        return self._instance.face_cascade.detectMultiScale(image, scaleFactor, minNeighbors, minSize)


def detect_faces(image_bytes):
    try:
        # Инициализируем face_cascade внутри функции
        # Получаем абсолютный путь к файлу haarcascade_frontalface_default.xml
        cascade_path = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml') 

        face_cascade = FaceCascadeSingleton(cascade_path)

        # Открываем изображение с помощью Pillow
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_array = np.array(img)

        # Получаем размеры изображения
        height, width = img_array.shape[:2]

        # Проверяем размеры изображения
        if width < 20 or height < 20:  # Я поставила минимальный размер - 20x20 пикселей
            print("Image is too small.")
            return None

        # Преобразуем изображение в оттенки серого
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

        # Обнаруживаем лица на изображении
        try:
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        except cv2.error as e:
            print(f"OpenCV error during face detection: {e}")
            return None

        # Рисуем прямоугольники на изображении
        for (x, y, w, h) in faces:
            cv2.rectangle(img_array, (x, y), (x+w, y+h), (0, 255, 0), 2)  

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

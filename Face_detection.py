# -*- coding: utf-8 -*-
import io
import os
import numpy as np
from PIL import Image
import cv2

# �������� ��������� Singleton ��� FaceCascade
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
        # �������������� face_cascade ������ �������
        # �������� ���������� ���� � ����� haarcascade_frontalface_default.xml
        cascade_path = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml') 

        face_cascade = FaceCascadeSingleton(cascade_path)

        # ��������� ����������� � ������� Pillow
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_array = np.array(img)

        # �������� ������� �����������
        height, width = img_array.shape[:2]

        # ��������� ������� �����������
        if width < 20 or height < 20:  # � ��������� ����������� ������ - 20x20 ��������
            print("Image is too small.")
            return None

        # ����������� ����������� � ������� ������
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

        # ������������ ���� �� �����������
        try:
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        except cv2.error as e:
            print(f"OpenCV error during face detection: {e}")
            return None

        # ������ �������������� �� �����������
        for (x, y, w, h) in faces:
            cv2.rectangle(img_array, (x, y), (x+w, y+h), (0, 255, 0), 2)  

        # ����������� ����������� ������� � ������ PIL
        img_pil = Image.fromarray(img_array)

        # ������� ������ BytesIO ��� �������� ����������� � ������
        output_stream = io.BytesIO()

        # ��������� ����������� � ������� JPEG � BytesIO
        img_pil.save(output_stream, format='JPEG')

        # �������� �������� ������ �����������
        image_bytes = output_stream.getvalue()

        return image_bytes

    except Exception as e:
        print(f"Error detecting faces: {e}")
        return None

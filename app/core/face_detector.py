import cv2
import numpy as np
from typing import List, Tuple
import os

class FaceDetector:
    def __init__(self):
        # Загрузка предобученной модели
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        if self.face_cascade.empty():
            raise IOError('Не удалось загрузить каскад Хаара для обнаружения лиц')

    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        # Распознает лица на изображении
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return [(x, y, w, h) for (x, y, w, h) in faces]

    def draw_rectangles(self, image_path: str, face_locations: List[Tuple[int, int, int, int]], output_path: str):
        # Рисует прямоугольники  и сохраняет результат
        try:
            image = cv2.imread(image_path)
            if image is None:
                print(f"Не удалось загрузить изображение для рисования прямоугольников: {image_path}")
                return

            for (x, y, w, h) in face_locations:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imwrite(output_path, image)
            print(f"Результат сохранен в: {output_path}")

        except Exception as e:
            print(f"Ошибка при рисовании прямоугольников: {e}")

class FaceDetectorFactory:
    @staticmethod
    def create_detector() -> FaceDetector:
        return FaceDetector()

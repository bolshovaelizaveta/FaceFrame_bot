import logging
from typing import List, Tuple

from sqlalchemy.orm import Session

from app.core.face_detector import FaceDetectorFactory
from app.schemas import image as image_schema
import os
import cv2
import numpy as np
import urllib.parse

class DetectionService:
    def __init__(self, db: Session):
        self.db = db
        self.face_detector = FaceDetectorFactory.create_detector()
        logging.info("Модель распознавания лиц успешно загружена")

    def process_image(self, image_path: str, filename: str) -> Tuple[int, List[image_schema.FaceCoords]]:
        # Обрабатывает изображение для распознавания лиц и сохранения данных о лицах
        try:
            #  Обработка имен файлов с кодировкой
            file_path_encoded = urllib.parse.quote(image_path)
            image = cv2.imread(file_path_encoded)
            if image is None:
                logging.warning(f"Не удалось загрузить изображение: {image_path}")
                return 0, []

            face_locations = self.face_detector.detect_faces(image)

            face_coords_list = []
            for (x, y, w, h) in face_locations:
                face_coords_list.append(image_schema.FaceCoords(x=x, y=y, width=w, height=h))

            return len(face_locations), face_coords_list

        except Exception as e:
            logging.error(f"Ошибки обработки файлов в process_image: {e}")
            return 0, []

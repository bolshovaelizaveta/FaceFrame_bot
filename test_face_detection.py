
import unittest
import io
from PIL import Image
import numpy as np
from Face_detection import detect_faces

class TestFaceDetection(unittest.TestCase):

    def test_detect_faces_valid_image(self):
        # Создаем тестовое изображение (черный квадрат)
        image = Image.new('RGB', (100, 100), color='black')
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes = image_bytes.getvalue()

        # Вызываем функцию detect_faces
        result = detect_faces(image_bytes)

        # Проверяем, что функция вернула что-то (изображение)
        self.assertIsNotNone(result)

        # Проверяем, что возвращенный результат является байтовой строкой
        self.assertIsInstance(result, bytes)

    def test_detect_faces_no_faces(self):
        # Создаем тестовое изображение (черный квадрат)
        image = Image.new('RGB', (100, 100), color='black')
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes = image_bytes.getvalue()

        # Вызываем функцию detect_faces
        result = detect_faces(image_bytes)

        # Если нет лиц, функция все равно должна вернуть изображение
        self.assertIsNotNone(result)

    def test_detect_faces_invalid_image(self):
        # Создаем невалидные байты изображения
        invalid_image_bytes = b"This is not an image"

        # Вызываем функцию detect_faces
        result = detect_faces(invalid_image_bytes)

        # Проверяем, что функция вернула None в случае ошибки
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()

import unittest
import io
from PIL import Image
import numpy as np
from Face_detection import detect_faces

class TestFaceDetection(unittest.TestCase):

    def test_detect_faces_valid_image(self):
        # ������� �������� ����������� (������ �������)
        image = Image.new('RGB', (100, 100), color='black')
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes = image_bytes.getvalue()

        # �������� ������� detect_faces
        result = detect_faces(image_bytes)

        # ���������, ��� ������� ������� ���-�� (�����������)
        self.assertIsNotNone(result)

        # ���������, ��� ������������ ��������� �������� �������� �������
        self.assertIsInstance(result, bytes)

    def test_detect_faces_no_faces(self):
        # ������� �������� ����������� (������ �������)
        image = Image.new('RGB', (100, 100), color='black')
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes = image_bytes.getvalue()

        # �������� ������� detect_faces
        result = detect_faces(image_bytes)

        # ���� ��� ���, ������� ��� ����� ������ ������� �����������
        self.assertIsNotNone(result)

    def test_detect_faces_invalid_image(self):
        # ������� ���������� ����� �����������
        invalid_image_bytes = b"This is not an image"

        # �������� ������� detect_faces
        result = detect_faces(invalid_image_bytes)

        # ���������, ��� ������� ������� None � ������ ������
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
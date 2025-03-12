import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)

def test_detect_faces_success():
    # Тест успешного обнаружения лиц
    with open("images/1.jpg", "rb") as f:  
        files = {"files": ("1.jpg", f)}
        response = client.post("/api/detect_faces/", files=files)

    assert response.status_code == 200
    data = response.json()
    assert "image_base64" in data
    assert "face_locations" in data
    assert "message" in data
    assert isinstance(data["face_locations"], list)  # Проверяем, что face_locations - список

def test_detect_faces_no_faces():
    # Тест обнаружения лиц, когда лиц нет на изображении
    with open("images/no_faces.jpg", "rb") as f:  
        files = {"files": ("no_faces.jpg", f)}
        response = client.post("/api/detect_faces/", files=files)

    assert response.status_code == 200
    data = response.json()
    assert "image_base64" in data
    assert "face_locations" in data
    assert "message" in data
    assert data["face_locations"] == []  # Проверяем, что список пуст
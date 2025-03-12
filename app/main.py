from fastapi import FastAPI, UploadFile, File, Depends, Request
from fastapi.exceptions import HTTPException
from typing import List
import logging
import shutil
from fastapi.middleware.cors import CORSMiddleware
from app.core.face_detector import FaceDetectorFactory
import os
import cv2
import io
from PIL import Image
import base64
from sqlalchemy.orm import Session
from app.db import models
from app.db.database import get_db
from app.schemas import image as image_schema
from app.core.detection_service import DetectionService
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import numpy as np

app = FastAPI()

logging.basicConfig(level=logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.abspath("static")  
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")  # Подключаем статические файлы

templates = Jinja2Templates(directory="app/templates")  # Указываем папку с шаблонами

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/upload", response_class=HTMLResponse)
async def upload_image(request: Request, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    # Загружает изображение, распознает лица и возвращает результаты
    detection_service = DetectionService(db)

    if files:
        try:
            file = files[0]  # Предполагаем, что загружается только один файл
            if not os.path.exists("images"):
                os.makedirs("images")

            file_path = f"images/{file.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            logging.debug(f"Filename: {file.filename} saved")

            faces_detected, face_locations = detection_service.process_image(file_path, file.filename)  # DetectionService

            if faces_detected > 0:
                message = f"На фотографии {faces_detected} лиц. Их координаты можно посмотреть в тг-канале или в базе данных."

                #  Сохраняем координаты лиц в базу данных
                for face in face_locations:
                    new_face = models.Face(
                        filename=file.filename,
                        x=face.x,
                        y=face.y,
                        width=face.width,
                        height=face.height
                    )
                    db.add(new_face)
                db.commit()
                logging.info(message)
            else:
                message = "На фотографии не обнаружено лиц."
                logging.info(message)
            return templates.TemplateResponse("index.html", {"request": request, "result": {"message": message}}) # Передаем result в шаблон
        except Exception as e:
            logging.error(f"Ошибки при обработке файлов: {e}")
            message = f"Ошибка при обработке файла: {e}"
            return templates.TemplateResponse("index.html", {"request": request, "result": {"message": message}})
    else:
        message = "Пожалуйста, выберите файл."
        return templates.TemplateResponse("index.html", {"request": request, "result": {"message": message}})

@app.post("/api/detect_faces/", response_model=image_schema.ImageUploadResponse)
async def detect_faces_api(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    # Распознает лица на заданном изображении, сохраняет данные в базе данных и возвращает координаты и изображение с прямоугольниками

    logging.debug(f"Полученные файлы: {files}")
    if files:
        try:
            file = files[0]
            if not os.path.exists("images"):
                os.makedirs("images")

            file_path = f"images/{file.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            logging.debug(f"Filename: {file.filename} saved")

            detection_service = DetectionService(db)
            faces_detected, face_locations = detection_service.process_image(file_path, file.filename)

            # Прямоугольники на изображении
            if faces_detected > 0:
                
                image = cv2.imread(file_path)
                for face in face_locations:
                    # Убеждаемся, что x, y, width и height - целые числа
                    x, y, w, h = int(face.x), int(face.y), int(face.width), int(face.height)
                    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2) 
                cv2.imwrite("images/detected_" + file.filename, image)
                # Кодируем изображение в base64
                encoded, buffer = cv2.imencode('.jpg', image)
                image_base64 = base64.b64encode(buffer).decode('utf-8')


                logging.info(f"Обнаружено {faces_detected} лиц в файле {file.filename}")

                #  Сохраняем координаты лиц в базу данных
                for face in face_locations:
                    new_face = models.Face(
                        filename=file.filename,
                        x=face.x,
                        y=face.y,
                        width=face.width,
                        height=face.height
                    )
                    db.add(new_face)
                db.commit()
                logging.info("Координаты лиц сохранены в базу данных.")

            else:
                logging.info(f"В файле не обнаружено лиц {file.filename}")
                image_base64 = None 

            return image_schema.ImageUploadResponse(
                filename=file.filename,
                faces_detected=faces_detected,
                face_locations=face_locations,
                message=f"Файлы успешно сохранены, всего обнаружено {faces_detected} лиц. Все координаты лиц сохранены в нашу базу данных facedetection", 
                image_base64=image_base64
            )
        except Exception as e:
            logging.error(f"Ошибка при обработке файла: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    else:
        logging.warning("Никакие файлы не были загружены.")
        raise HTTPException(status_code=400, detail="Никакие файлы не были загружены.")

from app.db.database import engine
from app.db import models

models.Base.metadata.create_all(bind=engine)


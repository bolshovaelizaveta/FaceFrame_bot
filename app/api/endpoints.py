from fastapi import APIRouter, UploadFile, File, Depends
from typing import List
import logging
import shutil
from app.core.face_detector import FaceDetector
import os
import cv2
import io
from PIL import Image
import base64
from sqlalchemy.orm import Session
from app.db import models
from app.db.database import get_db
from app.schemas import image as image_schema
from fastapi.exceptions import HTTPException

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Face Detection API"}


@router.post("/detect_faces/", response_model=image_schema.ImageUploadResponse)
async def detect_faces(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    # Распознает лица на заданном изображении, сохраняет данные в базе данных и возвращает координаты

    logging.debug(f"Полученные файлы: {files}")
    if files:
        try:
            faces_detected = 0
            face_locations = [] 
            image_base64 = None

            for file in files:
                if not os.path.exists("images"):
                    os.makedirs("images")

                file_path = f"images/{file.filename}"
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                logging.debug(f"Filename: {file.filename} saved")

                # Face detection
                face_detector = FaceDetector()
                faces = face_detector.detect_faces(file_path)
                faces_detected += len(faces)

                # Сохранить в базе данных
                db_image = models.Image(filename=file.filename, faces=len(faces))
                db.add(db_image)
                db.commit()
                db.refresh(db_image) 

                for (x, y, w, h) in faces:
                    db_face = models.Face(image_id=db_image.id, x=x, y=y, width=w, height=h)
                    db.add(db_face)
                    face_locations.append(image_schema.FaceCoords(x=x, y=y, width=w, height=h)) 

                if faces:
                    logging.info(f"Обнаружено {len(faces)} лиц в файле {file.filename}")
                    output_path = f"images/detected_{file.filename}"
                    face_detector.draw_rectangles(file_path, faces, output_path)
                    #  Encoding images into base64
                    with open(output_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
                    image_base64 = f"data:image/jpeg;base64,{encoded_string}"

                else:
                    logging.info(f"В файле не обнаружено лиц {file.filename}")

            return image_schema.ImageUploadResponse(
                filename=file.filename,
                faces_detected=faces_detected,
                face_locations=face_locations, 
                message=f"Файлы успешно сохранены, всего обнаружено {faces_detected} лиц", 
                image_base64=image_base64
            )

        except Exception as e:
            logging.error(f"File processing errors: {e}")
            raise HTTPException(status_code=500, detail=str(e))  # Raising exceptions for the error handler
    else:
        logging.warning("No files were uploaded.")
        raise HTTPException(status_code=400, detail="No files were uploaded.") # Raising exceptions for the error handler


from pydantic import BaseModel
from typing import List, Optional

class FaceCoords(BaseModel):
    x: int
    y: int
    width: int
    height: int

class ImageUploadResponse(BaseModel):
    filename: str
    faces_detected: int
    face_locations: List[FaceCoords]
    message: str
    image_base64: Optional[str] = None  

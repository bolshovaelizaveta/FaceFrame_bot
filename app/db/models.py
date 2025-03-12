from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    faces = Column(Integer, default=0) # Количество лиц

class Face(Base):
    __tablename__ = "faces"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)  # Добавлено поле filename
    x = Column(Integer)
    y = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Определяем переменные окружения
TELEGRAM_BOT_TOKEN = os.getenv("7743293848:AAHS_4Z_0YTILZXXnUWT1F0MxJSoGdNa5FU")
DATABASE_URL = os.getenv("postgresql://myuser:356786@localhost:1024/facedetection")

# Дополнительные настройки (пока оставим заглушки)
FACE_DETECTION_MODEL_PATH = os.getenv("FACE_DETECTION_MODEL_PATH", "models/haarcascade_frontalface_default.xml")

import telebot
import requests
import json  
import base64
import io
from PIL import Image

# Токен будет в сообщении с ссылкой на гитхаб
BOT_TOKEN = "" 
bot = telebot.TeleBot(BOT_TOKEN)

# URL конечной точки к API для распознавания лиц
API_URL = "http://127.0.0.1:8000/api/detect_faces/"


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот-стажер, созданный для учебного проекта по Python. Не ждите от меня многого, но лица я ищу неплохо! Отправьте изображение, чтобы проверить.")

@bot.message_handler(content_types=['photo'])
def echo_photo(message):
    try:
        # 1. Получаем информацию о фотографии
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        image_file = io.BytesIO(downloaded_file)

        # 2. Отправляем изображение в API
        files = {'files': ("image.jpg", image_file)}  
        response = requests.post(API_URL, files=files)

        if response.status_code == 200:
            try:
                data = response.json()
                print("Ответ API:", json.dumps(data, indent=4))  # Выводим весь ответ

                image_base64 = data.get("image_base64")  # Получаем image_base64
                face_locations = data.get("face_locations", [])
                api_message = data.get("message", "Не удалось обработать изображение.")  # Получаем сообщение от API

                # Отправляем изображение 
                if image_base64:
                    try:
                        image_bytes = base64.b64decode(image_base64)
                        image = io.BytesIO(image_bytes)
                        bot.send_photo(message.chat.id, photo=image)
                    except Exception as e:
                        bot.send_message(message.chat.id, f"Ошибка при обработке изображения: {e}")
                        print(f"Ошибка при обработке изображения: {e}")
                else:
                    bot.send_message(message.chat.id, "Не удалось получить изображение с рамками.")

                # Формируем сообщение с координатами
                message_text = api_message + "\n"  
                if face_locations:
                    message_text += f"Обнаружено {len(face_locations)} лиц.\n"
                    for i, face in enumerate(face_locations):
                        x = face.get("x")
                        y = face.get("y")
                        width = face.get("width")
                        height = face.get("height")

                        if x is not None and y is not None and width is not None and height is not None:
                            message_text += f"Лицо {i+1}: x={x}, y={y}, width={width}, height={height}\n"
                        else:
                            message_text += f"Не удалось получить координаты лица {i+1}\n"  # Сообщаем о пропущенных полях

                bot.send_message(message.chat.id, message_text) # Отправляем сообщение

            except json.JSONDecodeError as e:
                bot.send_message(message.chat.id, f"Ошибка при декодировании JSON: {e}\nОтвет сервера: {response.text}")
                print(f"Ошибка при декодировании JSON: {e}")
                print(f"Ответ сервера: {response.text}")
            except Exception as e:
                bot.send_message(message.chat.id, f"Общая ошибка при обработке ответа: {e}")
                print(f"Общая ошибка при обработке ответа: {e}")

        else:
            bot.send_message(message.chat.id, f"Ошибка API: {response.status_code}\nОтвет сервера: {response.text}")
            print(f"Ошибка API: {response.status_code}")
            print(f"Ответ сервера: {response.text}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла общая ошибка: {e}")
        print(f"Произошла общая ошибка: {e}")

bot.infinity_polling()
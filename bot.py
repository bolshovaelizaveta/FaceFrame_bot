# -*- coding: utf-8 -*-
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from Face_detection import detect_faces  


# API-токен бота
TOKEN = "Скину в личку"

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Я бот для обнаружения лиц. Отправьте мне изображение, и я найду лица на нем.")

# Обработчик команды /help
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Отправьте мне изображение, чтобы обнаружить лица. Используйте команду /detect.")

# Обработчик команды /detect
async def detect_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Отправьте изображение, чтобы обнаружить лица.")


# Обработчик изображений
async def detect(update: Update, context: CallbackContext) -> None:
    print("Функция detect вызвана!")
    print(f"update.message.photo: {update.message.photo}")

    if update.message.photo:
        print("Получено фото!")
        try:
            file_id = update.message.photo[-1].file_id
            file = await context.bot.get_file(file_id)
            image_bytes = await file.download_as_bytearray()  # Получаем изображение в виде байтов

            processed_image = detect_faces(image_bytes)

            if processed_image:
                # Отправляем изображение обратно пользователю
                await context.bot.send_photo(chat_id=update.message.chat_id, photo=processed_image)
            else:
                await update.message.reply_text("Лица не обнаружены или произошла ошибка.")

        except Exception as e:
            await update.message.reply_text(f"Произошла ошибка: {e}")

    elif update.message.text:
        print("Получен текст!")
        await update.message.reply_text("Я умею обрабатывать только фотографии, а не текст.")
    else:
        print("Получен другой тип файла!")
        await update.message.reply_text("Я умею обрабатывать только фотографии.")


def main() -> None:
    # Создаем объект Application
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("detect", detect_command)) 
    application.add_handler(MessageHandler(filters.PHOTO, detect))

    # Запускаем бота
    application.run_polling()


if __name__ == '__main__':
    main()
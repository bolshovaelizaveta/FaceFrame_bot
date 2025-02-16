# Telegram-бот Face_Detection

Это Telegram-бот, который обнаруживает лица на изображениях с использованием OpenCV и бэкенд API, построенного на FastAPI. Бот позволяет пользователям отправлять изображения и получать координаты обнаруженных лиц прямо в Telegram.

## Как это работает

1.  Пользователь отправляет изображение Telegram-боту.
2.  Бот пересылает изображение бэкенд API.
3.  Бэкенд API использует OpenCV для обнаружения лиц на изображении.
4.  Бэкенд API сохраняет координаты обнаруженных лиц в базе данных PostgreSQL.
5.  Бот получает координаты обнаруженных лиц от бэкенд API.
6.  Бот отправляет сообщение пользователю с координатами обнаруженных лиц.

## Основные технологии

*   **Telegram Bot API:** Позволяет боту взаимодействовать с пользователями Telegram.
*   **python-telegram-bot:** Python-библиотека для взаимодействия с Telegram Bot API.
*   **FastAPI (опционально):** Современный, высокопроизводительный веб-фреймворк для создания бэкенд API на Python (используется для обработки и хранения данных).
*   **OpenCV:** Библиотека компьютерного зрения для обнаружения лиц.
*   **PostgreSQL:** Реляционная база данных для хранения информации о лицах.
*   **psycopg2:** Python-адаптер для работы с PostgreSQL.

![alt text](bot_screen.jpg)

## Установка

1.  **Клонируйте репозиторий:** 

    ```bash
    git clone Project_python
    ```

2.  **Создайте виртуальное окружение:** 

    ```bash
    python -m venv venv
    ```

3.  **Активируйте виртуальное окружение:** 

    *   Windows:

        ```bash
        venv\Scripts\activate
        ```

    *   macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4.  **Установите зависимости:** 

    ```bash
    pip install -r requirements.txt
    ```

5.  **Установите библиотеку `python-telegram-bot`:**

    ```bash
    pip install python-telegram-bot
    ```


6.  **Получите API-токен Telegram-бота:**
    Отправлю в ЛС по запросу, чтобы не хранить его здесь.

## Запуск бота

1.  Замените `YOUR_BOT_TOKEN` на ваш фактический API-токен.
2.  Запустите бота:

    ```bash
    python telegram_bot.py
    ```

## Команды бота

*   `/start`: Отображает приветственное сообщение и описание бота.
*   Отправьте изображение: Бот обнаружит лица на изображении и вернет изображение с лицами, отмеченными зелеными прямоугольниками.

![alt text](screenshot/Test_bot.jpg)

![alt text](screenshot/validation_bot.jpg)

![alt text](screenshot/table_PostgreSQL.png)

![alt text](screenshot/Pytest.jpg)

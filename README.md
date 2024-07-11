# Homework Bot

## Описание проекта

`Homework Bot` — это бот для Telegram, который периодически опрашивает API сервиса "Практикум.Домашка" и уведомляет пользователя о статусе проверки домашней работы. Бот помогает своевременно получать информацию о результате ревью и оперативно узнавать, когда домашняя работа проверена или возвращена на доработку.

## Автор

Автор проекта: Denis Makhnach

## Технологии

Проект реализован с использованием следующих технологий:

- Python 3.8+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) — библиотека для работы с API Telegram
- [requests](https://docs.python-requests.org/en/latest/) — библиотека для отправки HTTP-запросов
- [dotenv](https://github.com/theskumar/python-dotenv) — библиотека для работы с переменными окружения
- [logging](https://docs.python.org/3/library/logging.html) — модуль для логирования

## Установка и запуск

### Предварительные требования

- Установленный Python версии 3.8 и выше.
- Созданный бот в Telegram и полученный токен API от [BotFather](https://core.telegram.org/bots#botfather).
- Токен для API сервиса "Практикум.Домашка".

### Шаги установки


1. Создайте и активируйте виртуальное окружение (опционально):

   ```sh
   python -m venv venv
   source venv/bin/activate
   ```
2. Установите необходимые зависимости:

   ```sh
   pip install -r requirements.txt
   ```
3. Создайте файл `.env` в корневой директории проекта и добавьте в него ваши токены:

   ```sh
   PRACTICUM_TOKEN=ваш_токен_практикума
   TELEGRAM_TOKEN=ваш_токен_телеграм
   TELEGRAM_CHAT_ID=ваш_telegram_chat_id
   ```

### Запуск

Для запуска бота выполните команду:

```sh
python homework.py
```

python telegram bot

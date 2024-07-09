import logging
import os
import sys
import requests
import time

from dotenv import load_dotenv
from telebot import TeleBot


load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Функция проверки наличия критические важных данный."""
    required_tokens = {
        'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
    }
    missing_tokens = [key for key, value in required_tokens.items()
                      if value is None]

    if missing_tokens:
        logging.critical(f"Отсутствуют следующие токены: \
                         {', '.join(missing_tokens)}")
        sys.exit(1)


def send_message(bot, message):
    """Функция отправки сообщения пользователю."""
    bot.send_message(TELEGRAM_CHAT_ID, message)
    logging.debug('Бот отравил сообщение пользователю.')


def get_api_answer(timestamp):
    """Функция для отправки GET-запроса на практикум."""
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        if response.status_code != 200:
            logging.error(f'Произошла ошибка при запросе:\
                          {response.status_code}')
            raise
        return response.json()
    except requests.RequestException:
        return None


def check_response(response):
    """Функция проверки наличия работ."""
    if 'homeworks' not in response or not isinstance(response['homeworks'],
                                                     list):
        raise TypeError('Неверный ответ от API')
    return response['homeworks']


def parse_status(homework):
    """Функция проверки статуса у работы."""
    if 'homework_name' not in homework:
        raise KeyError('Отсутствует название работы.')
    status = homework['status']
    if status not in HOMEWORK_VERDICTS:
        raise ValueError(f'Unexpected status value: {status}')
    homework_name = homework['homework_name']
    verdict = HOMEWORK_VERDICTS[status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    check_tokens()
    logging.debug('Все токены прошли проверку.')
    # Создаем объект класса бота
    bot = TeleBot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(timestamp)
            logging.debug('Запрос на API прошел успешно.')
            homeworks = check_response(response)
            if homeworks:
                message = parse_status(homeworks[0])
                send_message(bot, message)
            timestamp = response.get('current_date', timestamp)
        except Exception as error:
            logging.error(f'Ошибка в работе main функции: {error}')
            message = f'Сбой в работе программы: {error}'
            send_message(bot, message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()

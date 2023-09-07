import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

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
    """Проверка доступности переменных окружения."""
    tokens_ids = {
        'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID
    }
    missing = []
    for i in tokens_ids:
        if tokens_ids[i] is None:
            missing.append(i)
    if len(missing) != 0:
        logging.critical(
            f'Отсутствуют обязательные переменные окружения {missing}'
        )
        raise SystemExit('Программа принудительно остановлена')
    logging.debug('Обязательные переменные окружения доступны')


def send_message(bot, message):
    """Отправка сообщения в Telegram чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug(
            'Сообщение успешно отправлено пользователю Telegram-ботом'
        )
    except telegram.TelegramError as err:
        logging.error(f'Ошибка отправки сообщения Telegram-ботом - {err}')


def get_api_answer(timestamp):
    """Запрос к эндпоинту API-сервиса и получение ответа."""
    try:
        homework_statuses = requests.get(
            url=ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp}
        )
    except requests.RequestException:
        raise Exception('Ошибка при запросе к API-сервису')

    if homework_statuses.status_code != requests.codes.ok:
        raise requests.HTTPError('Не получен ответ от API-сервиса')

    logging.info('Получен ответ от API-сервиса')
    return homework_statuses.json()


def check_response(response):
    """Проверка ответа API-сервиса на соответствие требованиям."""
    if response is None:
        raise ValueError('Ответ API-сервиса не содержит данных')
    if not isinstance(response, dict):
        raise TypeError('Неверный формат данных ответа API-сервиса')
    if 'homeworks' not in response:
        raise KeyError('Ответ API-сервиса не содержит ключа "homeworks"')
    if not isinstance(response['homeworks'], list):
        raise TypeError('Неверный формат списка домашних работ')
    if len(response['homeworks']) == 0:
        raise ValueError('Нет домашних работ на проверке')
    logging.debug('Данные из ответа API-сервиса соответствуют требованиям')


def parse_status(homework):
    """Извлечение из полученных данных статуса домашней работы."""
    homework_name = homework.get('homework_name')
    status = homework.get('status')

    if homework_name is None:
        raise KeyError('В полученных данных отсутствует ключ "homework_name"')
    if status not in HOMEWORK_VERDICTS:
        raise KeyError('В полученных данных непредвиденный статус')
    verdict = HOMEWORK_VERDICTS[status]
    return (f'Изменился статус проверки работы "{homework_name}". {verdict}')


def main():
    """Основная логика работы бота."""
    logging.info('Программа начала работу')
    check_tokens()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    previous_message = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            check_response(response)
            homework = response['homeworks'][0]
            message = parse_status(homework)
        except Exception as err:
            message = f'Сбой в работе программы: {err}'
            logging.error(message)

        if message != previous_message:
            send_message(bot, message)
            previous_message = message
        else:
            logging.debug(
                'Сообщение не изменилось. Сообщение не отправлено'
            )

        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        encoding='utf-8',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()],
        level=logging.DEBUG
    )
    try:
        main()
    except KeyboardInterrupt:
        logging.info('Программа остановлена вручную')

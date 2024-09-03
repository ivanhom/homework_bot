# Homework Status Bot

Этот бот для Telegram предназначен для получения информации о статусе вашей домашней работы на сервисе "Практикум.Домашка". Он автоматически уведомляет вас о том, взята ли ваша работа на ревью, проверена ли она, а если проверена — принял её ревьюер или вернул на доработку.

## Требования

Для работы бота необходимы следующие переменные окружения:

- `PRACTICUM_TOKEN`: Перейдите по [этой ссылке](https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a), чтобы получить токен доступа к API "Практикум.Домашка".
- `TELEGRAM_TOKEN`: Создайте нового бота у `@BotFather` и получите API токен.
- `TELEGRAM_CHAT_ID`: Узнайте свой ID в Telegram с помощью `@userinfobot`.

## Настройка

1. Склонируйте репозиторий с ботом на ваш локальный компьютер:

   ```shell
   git clone git@github.com:ivanhom/homework_bot.git
   cd homework_bot
   ```

2. Установите виртуальное окружение и активируйте его:

    - Для linux/mac:
        ```shell
        python3 -m venv venv
        source venv/bin/activate
        ```
    - Для Windows:
        ```shell
        python -m venv venv
        .\venv\Scripts\activate
        ```

3. Установите необходимые зависимости:

    ```shell
    pip install -r requirements.txt
    ```

4. Создайте файл `.env` в корневой директории проекта и добавьте в него следующие строки:

    ```shell
    PRACTICUM_TOKEN=ваш_токен_практикум_домашка
    TELEGRAM_TOKEN=ваш_токен_телеграм
    TELEGRAM_CHAT_ID=ваш_чат_id
    ```

5. Для запуска бота запустите файл `homework.py`:

    ```shell
    python homework.py
    ```

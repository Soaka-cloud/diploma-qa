# Автотесты дипломного проекта: Yougile

Автоматизация тестирования системы управления проектами [Yougile](https://yougile.com):
веб-интерфейс (Selenium) и REST API v2 (Requests). Отчёты — Allure.

## Стек

- Python 3.11
- pytest
- Selenium (Selenium Manager, драйверы скачиваются автоматически)
- Requests
- allure-pytest

## Установка

```bash
pip install -r requirements.txt
```

## Настройка

Скопируйте `.env.example` в `.env` и заполните данные аккаунта Yougile:

```
YOUGILE_LOGIN=ваш_email
YOUGILE_PASSWORD=ваш_пароль
YOUGILE_KEY=опционально_готовый_токен
BROWSER=chrome
```

`BROWSER` принимает значения `chrome`, `edge` или `firefox`.
Если задан `YOUGILE_KEY`, API-тесты используют его напрямую;
иначе токен запрашивается через `POST /api-v2/auth/keys/get`.

## Запуск тестов

```bash
pytest
```

Тесты, требующие авторизации, автоматически пропускаются,
если данные аккаунта не заданы.

## Allure-отчёт

```bash
allure generate allure-results -o allure-report
allure open allure-report
```

## Структура

```
config.py          настройки из переменных окружения
yougile_api.py     клиент REST API v2
pages/             Page Object: login, dashboard, project, board
tests/test_api.py  API-тесты (авторизация, проекты)
tests/test_ui.py   UI-тесты (вход, проекты, задачи)
```

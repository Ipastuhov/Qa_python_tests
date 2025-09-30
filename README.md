## Технологии и стек
- Python 3.10+
- Pytest (+ параметризация, фикстуры)
- Playwright (UI, POM)
- Requests (API)
- Allure (отчёты)
- Pytest-xdist (параллельный запуск)

## Возможности фреймворка
- UI-тесты с Page Object Model
- API-тесты с ООП-обёртками поверх HTTP-клиента
- Общие фикстуры (браузер, контекст, страница, API клиент, логгер)
- Логирование в консоль и файл (`logs/tests.log`)
- Allure шаги и артефакты (трейсы Playwright, результаты тестов)

## Структура проекта
```text
project_python/
├─ src/
│  ├─ api/
│  │  ├─ client.py           # базовый HTTP-клиент (requests)
│  │  ├─ httpbin.py          # пример-обёртка (по желанию, отключаемо)
│  │  └─ task_manager.py     # обёртка API для локального task_manager-master
│  ├─ logging/
│  │  ├─ exceptions.py       # исключения фреймворка
│  │  └─ logger.py           # настройка логгера
│  └─ pages/
│     ├─ index_page.py       # POM: главная страница
│     ├─ create_page.py      # POM: создание задачи
│     ├─ detail_page.py      # POM: детали задачи
│     └─ edit_page.py        # POM: редактирование задачи
├─ tests/
│  ├─ api/
│  │  ├─ test_task_manager_api.py  # API-тесты к локальному Flask-приложению
│  │  └─ test_httpbin_api.py       # опциональные примеры (пропускаются по умолчанию)
│  ├─ ui/
│  │  ├─ test_task_manager_ui.py   # UI-тесты с POM
│  │  └─ test_ui_example.py        # пример
│  ├─ conftest.py                  # фикстуры (Playwright, API, логгер)
│  └─ data|fixtures                # при необходимости
├─ task_manager-master/            # демо-приложение Flask (локально)
├─ reports/                        # результаты тестов и отчёты Allure
├─ logs/                           # логи
├─ pytest.ini                      # конфиг Pytest
├─ requirements.txt                # зависимости
└─ README.md
```


## Переменные окружения
- `BASE_URL` — базовый URL веб-приложения для UI (по умолчанию `http://127.0.0.1:5000/`)
- `TASK_API_BASE_URL` — базовый URL API Task Manager (по умолчанию `http://127.0.0.1:5000/api`)
- `API_BASE_URL_HTTPBIN` — (необязательно) URL для httpbin; если НЕ задан, тесты httpbin будут пропущены


## Архитектура тестов
- UI: Page Object Model (`src/pages/*`), селекторы взяты из шаблонов `task_manager-master/templates`.
- API: обёртки `TaskManagerApi`, опционально `HttpBinApi`, используют общий `ApiClient` (логирование, обработка ошибок, таймауты). Все значения URL по умолчанию указывают на loopback и не ссылаются на внешние сервисы.
- Фикстуры: `tests/conftest.py` поднимает Playwright `browser/context/page`, включает Playwright tracing, предоставляет `api_client` и `logger`.
- Логирование: консоль + `logs/tests.log` (ротация файлов).
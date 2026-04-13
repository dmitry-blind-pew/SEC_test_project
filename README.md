# SEC Test Project

REST API справочника организаций, зданий и видов деятельности.

## Быстрый старт (Docker)

Поднять dev-контур:

```bash
docker compose up -d
```

Compose поднимет сервисы `db`, `redis`, `migrate`, `seed`, `app` и `db_test`.

После запуска открыть API:

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Для защищённых методов укажите заголовок X-API-Key (локально: super-secret-key, в Docker compose: dev-api-key).

## Тестовая БД (db_test)

Для интеграционных тестов используется отдельная БД:

- контейнер: `db_test`
- хост-порт: `5433`
- БД: `sectest_test`
- настройки в `.env-test`

## Локальный запуск тестов

1. Установить зависимости:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

2. Убедиться, что `db_test` запущена на `localhost:5433` (например, через `docker compose up -d`).
3. Запустить тесты:

```bash
pytest -q
```

`pytest.ini` уже настроен на использование `.env-test`.

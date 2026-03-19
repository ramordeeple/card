# Card REST API Service 💳

REST API для управления банковскими картами. Стек: FastAPI, PostgreSQL, SQLAlchemy 2.0, Alembic, JWT.

## Запуск

```bash
docker compose up --build
```

При старте контейнер автоматически применит миграции и создаст администратора — ничего делать вручную не нужно.

При необходимости отредактируйте `.env.example` перед запуском (логин/пароль админа, секрет JWT и параметры БД).

## Примеры запросов в `requests.http`

## Документация
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

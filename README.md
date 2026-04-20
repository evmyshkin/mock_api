# mock_api

![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)
![Python](https://img.shields.io/badge/python-3.13-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

FastAPI mock-сервис для интеграционного и workflow-тестирования.

Проект организован вокруг **3 первичных способов моков**:

- `setter`: strict/open запись данных и их выдача по GET
- `processor`: асинхронный submit/status флоу с управляемыми переходами статусов
- `proxy`: захват входящих запросов и хранение метаданных вызова

## Быстрый старт (Docker)

```bash
docker compose up -d
curl -s http://localhost:8000/healthcheck
docker compose down
```

## Публичный API

### Setter

- `POST /setter/api/v1/products/set`
- `POST /setter/api/v1/products/set-open`
- `GET /setter/api/v1/products`
- `DELETE /setter/api/v1/products`
- `DELETE /setter/api/v1/clear`
- `GET /setter/api/v1/requests`
- `GET /setter/settings`
- `PUT /setter/settings`

### Processor

- `POST /processor/api/v1/order`
- `GET /processor/api/v1/requests`
- `GET /processor/api/v1/status?request_id=...`
- `GET /processor/settings`
- `PUT /processor/settings`
- `GET /processor/settings/post-modes`
- `GET /processor/settings/status-modes`
- `GET /processor/settings/status-mode-steps`
- `PUT /processor/settings/status-mode-steps`

### Proxy

- `POST /proxy/api/v1/pay`
- `GET /proxy/api/v1/requests`
- `DELETE /proxy/api/v1/requests`
- `GET /proxy/api/v1/requests/{request_id}`
- `GET /proxy/settings`
- `PUT /proxy/settings`

### Service endpoints

- `GET /healthcheck`
- `GET /metrics` (не входит в OpenAPI)

## Паттерны мок-взаимодействий

| Паттерн | Endpoint(ы) | Назначение |
|---|---|---|
| Strict schema validation | `POST /setter/api/v1/products/set`, `POST /processor/api/v1/order` | Проверка структуры payload перед сохранением |
| Open schema payload | `POST /setter/api/v1/products/set-open` | Захват произвольного JSON |
| Delayed response | `PUT /setter/settings`, `PUT /processor/settings`, `PUT /proxy/settings` | Эмуляция задержки через `response_delay` |
| Forced status code | те же settings endpoints | Эмуляция HTTP-поведения через `response_code` |
| Async status transitions | scheduler + `GET /processor/api/v1/status` | Симуляция фоновой обработки во времени |
| Request capture | `POST /proxy/api/v1/pay`, `GET /proxy/api/v1/requests*` | Инспекция входящих интеграционных вызовов |

## База данных

### Схемы и таблицы

- `setter_schema`
  - `requests`
  - `settings`
- `processor_schema`
  - `requests`
  - `settings`
  - `post_modes`
  - `status_modes`
  - `status_mode_steps`
- `proxy_schema`
  - `requests`
  - `settings`

### Миграции

Линейная цепочка из трех ревизий:

1. `setter_schema`
2. `processor_schema`
3. `proxy_schema`

```bash
uv run alembic upgrade head
uv run alembic downgrade -1
```

## Нейминг моделей (рекомендация)

Чтобы одновременно сохранить бизнес-смысл и явно показать 3 типа моков, используем правило:

- в БД фиксируем generic-таблицы: `requests/settings/...`
- в Python-слое всегда префиксируем типом мока: `Setter*`, `Processor*`, `Proxy*`
- бизнес-поля внутри payload сохраняем предметными (`order_id`, `customer_id`, `product_id`), чтобы сценарии интеграции оставались читаемыми

Это дает прозрачность для тестовой платформы (по префиксу видно тип мока) и не теряет доменную выразительность данных.

## OpenAPI

- версионируемый файл: `docs/openapi/openapi.v1.json`
- экспорт:

```bash
uv run python scripts/export_openapi.py --output docs/openapi/openapi.v1.json
```

Swagger UI локально: `http://localhost:8000/docs`

## Локальная разработка

### Требования

- Python `3.13.11`
- [uv](https://docs.astral.sh/uv/)
- Docker (рекомендуется)

### Установка

```bash
uv sync --locked --dev
cp .env-example .env
uv run alembic upgrade head
uv run fastapi dev app/main.py
```

### Проверки качества

```bash
uv run ruff check .
uv run mypy .
uv run pytest -q
```

## Примеры внешних клиентов

- `httpx`: `docs/examples/httpx_quickstart.py`
- Postman: `docs/examples/postman/mock_api.postman_collection.json`

## Релизы и стабильность

- Процесс релиза: `docs/RELEASE.md`
- История изменений: `CHANGELOG.md`
- Политика безопасности: `SECURITY.md`

## Open Source управление

- Гайд по вкладу: `CONTRIBUTING.md`
- Кодекс поведения: `CODE_OF_CONDUCT.md`
- Лицензия: `LICENSE`

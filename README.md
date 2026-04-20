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

## Пошаговый туториал: 3 типа моков

Этот проект позволяет быстро поднять три разных вида моков под интеграционные сценарии:

- `setter` - когда нужно заранее подготовить данные и потом читать их по GET
- `processor` - когда нужен асинхронный submit/status поток с переходами статусов
- `proxy` - когда нужно перехватывать и инспектировать входящие вызовы от внешней системы

### Шаг 0. Подготовьте локальный стенд

```bash
docker compose up -d
curl -s http://localhost:8000/healthcheck
```

Если ответ `healthcheck` успешный, откройте Swagger UI: `http://localhost:8000/docs`

### 1) Setter: подготовка и выдача данных витрины

Что делает:

- сохраняет данные в strict-режиме (`/products/set`) или open-режиме (`/products/set-open`)
- отдает накопленные данные через `GET /setter/api/v1/products`
- дает отладочный снимок всех записей через `GET /setter/api/v1/requests`

Пошаговый сценарий:

```bash
BASE_URL=http://localhost:8000

# 1. Записать данные со строгой схемой
curl -s -X POST "$BASE_URL/setter/api/v1/products/set" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "product_id": "product-1",
      "sku": "sku-001",
      "name": "Demo Product",
      "category": "electronics",
      "price": 10.5,
      "currency": "USD",
      "quantity": 5
    }
  ]'

# 2. Записать данные по свободной схеме
curl -s -X POST "$BASE_URL/setter/api/v1/products/set-open" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "any_field": "value",
      "nested": {"k": "v"}
    }
  ]'

# 3. Прочитать агрегированные данные для pull-интеграции
curl -s "$BASE_URL/setter/api/v1/products"

# 4. Прочитать отладочный список всех сохраненных setter-запросов
curl -s "$BASE_URL/setter/api/v1/requests"
```

Настройка без кода (через settings):

```bash
# Посмотреть настройки
curl -s "$BASE_URL/setter/settings"

# Изменить задержку и HTTP-код ответа у endpoint-а
curl -s -X PUT "$BASE_URL/setter/settings" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "response_delay": 2,
    "response_code": 200
  }'
```

Как расширить setter под проект:

1. Добавить/изменить схему входного payload (`app/api/setter/schemas/...`).
2. Добавить бизнес-логику в сервис (`app/api/setter/services/setter_service.py`).
3. При необходимости расширить сохранение/чтение в DAO/моделях (`app/db/dao/setter_dao`, `app/db/models/setter_schema`).
4. Если нужна новая сущность или тип endpoint-настроек - добавить миграцию с seed-данными в `setter_schema.settings`.
5. Подключить роут в `app/api/setter/controllers/...` и проверить регистрацию в `app/api/router.py`.
6. Добавить API/unit-тесты для нового поведения.

### 2) Processor: submit/status с асинхронными переходами

Что делает:

- принимает заказ через `POST /processor/api/v1/order`
- возвращает `request_id`, по которому можно опрашивать статус
- переводит статусы автоматически в фоне (scheduler, каждые 5 секунд)

Пошаговый сценарий:

```bash
BASE_URL=http://localhost:8000

# 1. Отправить заказ в обработку
curl -s -X POST "$BASE_URL/processor/api/v1/order" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "order-1001",
    "customer_id": "customer-42",
    "items": [
      {"sku": "sku-001", "quantity": 1, "unit_price": 10.5}
    ],
    "total_amount": 10.5,
    "currency": "USD"
  }'

# 2. Скопировать request_id из ответа и опросить статус
curl -s "$BASE_URL/processor/api/v1/status?request_id=<REQUEST_ID>"

# 3. (Опционально) посмотреть все зарегистрированные запросы обработки
curl -s "$BASE_URL/processor/api/v1/requests"
```

Настройка без кода (через settings):

```bash
# Текущая конфигурация endpoint-ов submit/status
curl -s "$BASE_URL/processor/settings"

# Справочники режимов
curl -s "$BASE_URL/processor/settings/post-modes"
curl -s "$BASE_URL/processor/settings/status-modes"
curl -s "$BASE_URL/processor/settings/status-mode-steps"

# Обновить настройку endpoint-а (id возьмите из GET /processor/settings)
curl -s -X PUT "$BASE_URL/processor/settings" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "response_delay": 1,
    "response_code": 200,
    "status_mode_id": 1,
    "post_mode_id": 1
  }'

# Обновить длительность/ошибку конкретного шага статуса
curl -s -X PUT "$BASE_URL/processor/settings/status-mode-steps" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "duration": 10,
    "error_message": null
  }'
```

Как расширить processor под проект:

1. Изменить схему submit-платежа (`app/api/processor/schemas/requests/...`).
2. Добавить правила обработки в `app/api/processor/services/processor_service.py`.
3. Добавить/расширить режимы `post_modes`, `status_modes`, `status_mode_steps` через миграции и seed-данные.
4. Обновить DAO/модели processor-схемы (`app/db/dao/processor_dao`, `app/db/models/processor_schema`).
5. При необходимости скорректировать фоновые задачи в `app/scheduler/...`.
6. Добавить API/unit-тесты на submit/status и переходы по шагам.

### 3) Proxy: захват и отладка входящих интеграционных вызовов

Что делает:

- сохраняет тело запроса и метаданные (headers/query) по `request_id`
- дает список всех захваченных вызовов и чтение записи по `request_id`

Пошаговый сценарий:

```bash
BASE_URL=http://localhost:8000

# 1. Отправить внешний вызов в proxy-мок (request_id обязателен в header)
curl -s -X POST "$BASE_URL/proxy/api/v1/pay?channel=mobile" \
  -H "Content-Type: application/json" \
  -H "request_id: req-1001" \
  -d '{
    "amount": 1250,
    "currency": "USD",
    "payment_method": "card"
  }'

# 2. Получить все перехваченные запросы
curl -s "$BASE_URL/proxy/api/v1/requests"

# 3. Получить конкретный перехваченный запрос
curl -s "$BASE_URL/proxy/api/v1/requests/req-1001"
```

Настройка без кода (через settings):

```bash
# Текущие настройки proxy endpoint-а
curl -s "$BASE_URL/proxy/settings"

# Изменить задержку и HTTP-код ответа
curl -s -X PUT "$BASE_URL/proxy/settings" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "response_delay": 3,
    "response_code": 202
  }'
```

Как расширить proxy под проект:

1. Добавить нужные поля/правила в response-схемы proxy (`app/api/proxy/schemas/...`).
2. Расширить сбор и обработку метаданных в `app/api/proxy/services/proxy_service.py`.
3. Изменить модель хранения и DAO (`app/db/models/proxy_schema`, `app/db/dao/proxy_dao`) и добавить миграцию.
4. При добавлении новых capture endpoint-ов - реализовать контроллер и зарегистрировать роут в `app/api/router.py`.
5. Покрыть новые сценарии API/unit-тестами.

### Универсальный чеклист расширения любого мока

1. Описать API-контракт (request/response schema).
2. Реализовать/обновить бизнес-логику в service-слое.
3. Обновить DAO и DB-модели.
4. Подготовить миграцию и seed-данные настроек.
5. Подключить маршруты в router.
6. Добавить автотесты на happy-path и ошибки.
7. Перегенерировать OpenAPI-снапшот при изменении контракта.

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

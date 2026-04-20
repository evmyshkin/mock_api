# Локальная разработка
dev:
	uv run uvicorn app.main:fastapi_app --host 127.0.0.1 --port "8000" --reload
migrate:
	uv run alembic upgrade head
migrate-down:
	uv run alembic downgrade -1

# Docker разработка
db:
	docker compose up --build db -d
up:
	docker compose up -d
up-stack:
	docker compose up --build -d
down:
	docker compose down

# Запустить пре-коммит линтер и форматтер
lint:
	uv run pre-commit run --all-files

typecheck:
	uv run mypy .

test:
	uv run pytest --cov=app --cov-branch --cov-report=term-missing

check: lint typecheck test

openapi-export:
	uv run python scripts/export_openapi.py --output docs/openapi/openapi.v1.json

smoke:
	curl -s http://localhost:8000/healthcheck

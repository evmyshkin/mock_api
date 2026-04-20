# Тесты

## Запуск всех тестов

```bash
uv run pytest
```

## Отчет покрытия

```bash
uv run pytest --cov=app --cov-branch --cov-report=term-missing
```

## Smoke-набор

```bash
uv run pytest -m smoke
```

## Параллельный запуск (только для изолированных suite)

```bash
uv run pytest -n auto
```

Используйте xdist только когда тесты независимы и безопасны для параллельного запуска.

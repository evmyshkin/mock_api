# Процесс релиза

Проект использует релизы по git-тегам.

## Политика версионирования

- До `1.0.0`: best-effort стабильность, но все изменения публичного API должны быть отражены в `CHANGELOG.md`.
- Начиная с `1.0.0`: Semantic Versioning.

## Чеклист релиза

1. Убедитесь, что CI зеленый (`ruff`, `mypy`, `pytest`).
2. Обновите `CHANGELOG.md` (`[Unreleased]` -> новая секция версии).
3. Если API-контракт изменился, перегенерируйте OpenAPI:
   ```bash
   uv run python scripts/export_openapi.py --output docs/openapi/openapi.v1.json
   ```
4. Закоммитьте релизные изменения.
5. Создайте и отправьте тег:
   ```bash
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```
6. Проверьте, что GitHub release содержит OpenAPI-артефакт.

## Migration Notes

Если релиз меняет схему БД или API-контракт:

- добавьте короткое migration note в описание релиза
- перечислите id миграций Alembic
- явно опишите backward-incompatible изменения API

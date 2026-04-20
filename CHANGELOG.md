# История изменений

Все значимые изменения проекта фиксируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
а начиная с `1.0.0` проект следует [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Добавлено

- Базовая OSS-документация: `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`.
- GitHub Actions workflows для CI и публикации OpenAPI-артефакта релиза.
- Скрипт экспорта OpenAPI и версионируемый OpenAPI-контракт.
- Быстрый старт за 5 минут и документация по паттернам взаимодействия.
- Примеры интеграции (`httpx` и Postman collection).
- Contract-тесты для защиты согласованности публичного API.

### Изменено

- README обновлен для публичного OSS-использования и быстрого onboarding.
- Минимальная поддерживаемая версия Python в метаданных проекта снижена до `>=3.11`.
- Нейминг тестов приведен к публичным доменным именам вместо legacy `source_*`.

## [0.1.0] - 2026-04-19

### Добавлено

- Первый публичный релиз `mock_api` с доменами:
  - storefront
  - order processing
  - product upload

from fastapi import APIRouter

from app.api.extra_api.controllers.healthcheck import router as healthcheck_router
from app.api.extra_api.controllers.metrics import router as metrics_router
from app.api.processor.controllers.v1.processor_controller import router as processor_router
from app.api.proxy.controllers.v1.proxy_controller import router as proxy_router
from app.api.setter.controllers.setter_data_controller import router as setter_data_router
from app.api.setter.controllers.v1.setter_controller import router as setter_router
from app.api.settings.controllers.processor_settings_controller import router as processor_settings_router
from app.api.settings.controllers.proxy_settings_controller import router as proxy_settings_router
from app.api.settings.controllers.setter_settings_controller import router as setter_settings_router

router = APIRouter()

SETTER_TAG = 'Setter API. Наполняет данные витрины для pull-интеграций'
PROCESSOR_TAG = 'Processor API. Эмулирует асинхронную обработку и статусы'
PROXY_TAG = 'Proxy API. Захватывает запрос и хранит метаданные вызова'
SETTER_SETTINGS_TAG = 'Setter Settings. Настройка статус-кодов и задержек'
PROCESSOR_SETTINGS_TAG = 'Processor Settings. Настройка статус-кодов, задержек и статусов обработки'
PROXY_SETTINGS_TAG = 'Proxy Settings. Настройка статус-кодов и задержек'

router.include_router(
    setter_router,
    prefix='/setter/api/v1',
    tags=[SETTER_TAG],
)

router.include_router(
    setter_settings_router,
    prefix='/setter/settings',
    tags=[SETTER_SETTINGS_TAG],
)
router.include_router(
    processor_router,
    prefix='/processor/api/v1',
    tags=[PROCESSOR_TAG],
)
router.include_router(
    processor_settings_router,
    prefix='/processor/settings',
    tags=[PROCESSOR_SETTINGS_TAG],
)

router.include_router(
    proxy_router,
    prefix='/proxy/api/v1',
    tags=[PROXY_TAG],
)

router.include_router(
    proxy_settings_router,
    prefix='/proxy/settings',
    tags=[PROXY_SETTINGS_TAG],
)


router.include_router(
    setter_data_router,
    prefix='/setter/api/v1',
    tags=[SETTER_TAG],
)

router.include_router(
    healthcheck_router,
    prefix='',
    tags=['Проверка здоровья'],
)

router.include_router(
    metrics_router,
    prefix='',
    tags=['Метрики'],
)

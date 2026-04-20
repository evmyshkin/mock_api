from contextlib import asynccontextmanager
from typing import Any

import uvicorn

from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware

from app.api.fastapi_middlewares.logging_middleware import log_request_reponse
from app.api.processor.utils.processor_exception_handler import setup_processor_submit_exception_handler
from app.api.router import router as main_router
from app.config import config
from app.scheduler.factories import create_main_scheduler
from app.utils.docstrings import DocstringEnum
from app.utils.logger_setup import LoggerSetup


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    """Запуск логгера, шедуллера и Redis воркера.

    Args:
        app: Экземпляр FastAPI приложения

    Yields:
        None: Контекст менеджер для жизненного цикла приложения
        :type app: FastAPI
    """
    # Запуск логгера
    LoggerSetup.configure_logging()

    # Запускаем задачи планировщика для доменов витрины и обработки заказов
    scheduler = create_main_scheduler()

    try:
        yield
    finally:
        # Останавливаем шедуллер
        scheduler.shutdown(wait=True)


# FastAPI. Запускаем приложение.
fastapi_app = FastAPI(
    lifespan=lifespan,
    title='mock_api',
    description=DocstringEnum.MAIN_DOCSTRING,
    swagger_ui_parameters={
        'defaultModelsExpandDepth': -1,  # Прячем отображение схем внизу в Swagger
        'docExpansion': 'none',  # Сворачиваем все теги
    },
)

setup_processor_submit_exception_handler(fastapi_app)

fastapi_app.middleware('http')(log_request_reponse)


# Prometheus. Запускаем экспорт метрик.
fastapi_app.add_middleware(
    PrometheusMiddleware,
    app_name=config.common.project_name,
    prefix='fast_api',
    skip_methods=['OPTIONS', 'HEAD'],
    skip_paths=config.common.disabled_log_endpoints,
)

fastapi_app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run(fastapi_app, host='127.0.0.1', port=8000)

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api.processor.utils.processor_exceptions import ProcessorSubmitError


async def processor_submit_exception_handler(_request: Request, exc: ProcessorSubmitError) -> JSONResponse:
    """Обрабатывать эмулированные ошибки отправки для обработки заказов."""
    return JSONResponse(status_code=exc.status_code, content=exc.msg)


def setup_processor_submit_exception_handler(app: FastAPI) -> None:
    """Зарегистрировать обработчик исключений для эмулированных сбоев отправки."""
    app.add_exception_handler(ProcessorSubmitError, processor_submit_exception_handler)  # type: ignore[arg-type]

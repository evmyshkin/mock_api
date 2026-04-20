from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response

from app.api.dependencies.processor_service_deps import get_processor_service
from app.api.processor.schemas.requests.processor_submit_request_schema import ProcessorSubmitRequestSchema
from app.api.processor.schemas.responses.processor_request_response_schema import ProcessorRequestResponseSchema
from app.api.processor.schemas.responses.processor_status_response_schema import ProcessorStatusResponseSchema
from app.api.processor.schemas.responses.processor_submit_response_schema import ProcessorSubmitResponseSchema
from app.api.processor.services.processor_service import ProcessorService

router = APIRouter()
ProcessorServiceDep = Annotated[ProcessorService, Depends(get_processor_service)]


@router.post(
    '/order',
    summary='Отправить заказ в машину состояний обработки.',
    response_model_exclude_none=True,
)
async def submit_order(
    request: ProcessorSubmitRequestSchema,
    response: Response,
    service: ProcessorServiceDep,
) -> ProcessorSubmitResponseSchema:
    """Зарегистрировать новый запрос обработки заказа."""
    return await service.submit_order(request=request, res_obj=response)


@router.get(
    '/requests',
    summary='Получить сохраненные requests обработки заказов.',
)
async def get_requests(
    service: ProcessorServiceDep,
) -> list[ProcessorRequestResponseSchema]:
    """Вернуть сохраненные запросы обработки от новых к старым."""
    return await service.get_requests()


@router.get(
    '/status',
    summary='Получить статус обработки заказа по идентификатору запроса.',
    response_model_exclude_none=True,
)
async def get_order_status(
    request_id: str,
    response: Response,
    service: ProcessorServiceDep,
) -> ProcessorStatusResponseSchema:
    """Получить текущий статус обработки заказа."""
    return await service.get_order_status(request_id=request_id, res_obj=response)

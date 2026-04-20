from typing import Annotated
from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import Request
from fastapi import Response

from app.api.dependencies.proxy_deps import get_proxy_service
from app.api.proxy.schemas.responses.proxy_request_response_schema import ProxyRequestResponseSchema
from app.api.proxy.services.proxy_service import ProxyService
from app.api.setter.schemas.v1.setter_clear_response_schema import SetterClearResponseSchema

router = APIRouter()
ProxyServiceDep = Annotated[ProxyService, Depends(get_proxy_service)]


@router.post('/pay', summary='Перехватить информацию входящего запроса на платеж.')
async def capture_proxy(
    payload: dict[str, Any],
    request_id: Annotated[str, Header(convert_underscores=False)],
    request: Request,
    response: Response,
    service: ProxyServiceDep,
) -> ProxyRequestResponseSchema:
    """Сохранить метаданные запроса и payload по request_id."""
    return await service.capture_request(
        request=request,
        payload=payload,
        request_id=request_id,
        res_obj=response,
    )


@router.get('/requests', summary='Получить сохраненные proxy-запросы.')
async def get_requests(
    service: ProxyServiceDep,
) -> list[ProxyRequestResponseSchema]:
    """Вернуть сохраненные запросы в порядке от новых к старым."""
    return await service.get_records()


@router.get('/requests/{request_id}', summary='Получить proxy-запрос по request_id.')
async def get_proxy_record(
    request_id: str,
    service: ProxyServiceDep,
) -> ProxyRequestResponseSchema:
    """Вернуть одну сохраненную запись по request_id."""
    return await service.get_record(request_id=request_id)


@router.delete('/requests', summary='Полностью очистить proxy requests.')
async def clear_requests(
    service: ProxyServiceDep,
) -> SetterClearResponseSchema:
    """Удалить все сохраненные proxy requests."""
    return await service.clear_records()

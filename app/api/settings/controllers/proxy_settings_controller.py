from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies.settings_deps import get_proxy_settings_service
from app.api.settings.schemas.requests.base_settings_request_schema import BaseSettingsUpdateRequestSchema
from app.api.settings.schemas.responses.proxy_settings_response_schema import ProxySettingsResponseSchema
from app.api.settings.services.proxy_settings_service import ProxySettingsService

router = APIRouter()
ProxySettingsServiceDep = Annotated[
    ProxySettingsService,
    Depends(get_proxy_settings_service),
]


@router.get('', summary='Получить настройки proxy-эндпоинта.')
async def get_settings(service: ProxySettingsServiceDep) -> list[ProxySettingsResponseSchema]:
    """Вернуть список настроек proxy capture endpoint."""
    return await service.get_settings()


@router.put('', summary='Обновить настройку proxy-эндпоинта.')
async def update_proxy_setting(
    request: BaseSettingsUpdateRequestSchema,
    service: ProxySettingsServiceDep,
) -> ProxySettingsResponseSchema:
    """Обновить настройку proxy capture endpoint по id."""
    return await service.update_proxy_setting(values=request)

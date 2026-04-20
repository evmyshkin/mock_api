from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies.settings_deps import get_setter_settings_service
from app.api.settings.schemas.requests.base_settings_request_schema import BaseSettingsUpdateRequestSchema
from app.api.settings.schemas.responses.setter_settings_response_schema import SetterSettingsResponseSchema
from app.api.settings.services.setter_settings_service import SetterSettingsService

router = APIRouter()
SetterSettingsServiceDep = Annotated[SetterSettingsService, Depends(get_setter_settings_service)]


@router.get('', summary='Получить настройки setter-эндпоинтов.')
async def get_settings(service: SetterSettingsServiceDep) -> list[SetterSettingsResponseSchema]:
    """Получить настройки соединения setter API."""
    return await service.get_settings()


@router.put('', summary='Обновить настройку setter-эндпоинта.')
async def update_setter_setting(
    request: BaseSettingsUpdateRequestSchema,
    service: SetterSettingsServiceDep,
) -> SetterSettingsResponseSchema:
    """Обновить настройку соединения setter API по id."""
    return await service.update_setter_setting(values=request)

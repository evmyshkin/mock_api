from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies.settings_deps import get_processor_settings_service
from app.api.settings.schemas.requests.processor_settings_update_request_schema import (
    ProcessorSettingsUpdateRequestSchema,
)
from app.api.settings.schemas.requests.processor_status_mode_step_update_request_schema import (
    ProcessorStatusModeStepUpdateRequestSchema,
)
from app.api.settings.schemas.responses.processor_post_modes_response_schema import ProcessorPostModesResponseSchema
from app.api.settings.schemas.responses.processor_settings_response_schema import ProcessorSettingsResponseSchema
from app.api.settings.schemas.responses.processor_status_mode_steps_response_schemas import (
    ProcessorStatusModeStepsNamedResponseSchema,
)
from app.api.settings.schemas.responses.processor_status_mode_steps_response_schemas import (
    ProcessorStatusModeStepsResponseSchema,
)
from app.api.settings.schemas.responses.processor_status_modes_response_schema import ProcessorStatusModesResponseSchema
from app.api.settings.services.processor_settings_service import ProcessorSettingsService

router = APIRouter()
ProcessorSettingsServiceDep = Annotated[
    ProcessorSettingsService,
    Depends(get_processor_settings_service),
]


@router.get('', summary='Получить настройки processor-эндпоинтов.')
async def get_settings(service: ProcessorSettingsServiceDep) -> list[ProcessorSettingsResponseSchema]:
    """Вернуть список настроек processor API."""
    return await service.get_settings()


@router.put('', summary='Обновить настройку processor-эндпоинта.')
async def update_processor_setting(
    request: ProcessorSettingsUpdateRequestSchema,
    service: ProcessorSettingsServiceDep,
) -> ProcessorSettingsResponseSchema:
    """Обновить одну настройку уровня processor endpoint."""
    return await service.update_processor_setting(values=request)


@router.get('/post-modes', summary='Получить processor post-modes.')
async def get_post_modes(
    service: ProcessorSettingsServiceDep,
) -> list[ProcessorPostModesResponseSchema]:
    """Вернуть все post-modes для processor submit."""
    return await service.get_post_modes()


@router.get('/status-modes', summary='Получить processor status-modes.')
async def get_status_modes(
    service: ProcessorSettingsServiceDep,
) -> list[ProcessorStatusModesResponseSchema]:
    """Вернуть все режимы переходов статусов."""
    return await service.get_status_modes()


@router.get('/status-mode-steps', summary='Получить processor status-mode-steps.')
async def get_status_mode_steps(
    service: ProcessorSettingsServiceDep,
) -> list[ProcessorStatusModeStepsNamedResponseSchema]:
    """Вернуть все шаги статусов для всех режимов."""
    return await service.get_status_mode_steps()


@router.put('/status-mode-steps', summary='Обновить processor status-mode-step.')
async def update_status_mode_steps(
    request: ProcessorStatusModeStepUpdateRequestSchema,
    service: ProcessorSettingsServiceDep,
) -> ProcessorStatusModeStepsResponseSchema:
    """Обновить конфигурацию одного шага статуса по id."""
    return await service.update_status_mode_steps(values=request)

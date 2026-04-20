from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

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
from app.db.dao.processor_dao.processor_post_modes_dao import ProcessorPostModesDao
from app.db.dao.processor_dao.processor_settings_dao import ProcessorSettingsDao
from app.db.dao.processor_dao.processor_status_mode_steps_dao import ProcessorStatusModeStepsDao
from app.db.dao.processor_dao.processor_status_modes_dao import ProcessorStatusModesDao


class ProcessorSettingsService:
    """Сервис управления настройками обработки заказов."""

    def __init__(
        self,
        processor_settings_dao: ProcessorSettingsDao,
        processor_status_mode_steps_dao: ProcessorStatusModeStepsDao,
        processor_status_modes_dao: ProcessorStatusModesDao,
        processor_post_modes_dao: ProcessorPostModesDao,
        session: AsyncSession,
    ) -> None:
        self._processor_settings_dao = processor_settings_dao
        self._processor_status_mode_steps_dao = processor_status_mode_steps_dao
        self._processor_status_modes_dao = processor_status_modes_dao
        self._processor_post_modes_dao = processor_post_modes_dao
        self._session = session

    async def get_settings(self) -> list[ProcessorSettingsResponseSchema]:
        """Вернуть все настройки эндпоинтов обработки заказов."""

        settings = await self._processor_settings_dao.find_all_settings(session=self._session)
        return [ProcessorSettingsResponseSchema.model_validate(setting) for setting in settings]

    async def update_processor_setting(
        self,
        values: ProcessorSettingsUpdateRequestSchema,
    ) -> ProcessorSettingsResponseSchema:
        """Обновить одну настройку эндпоинта обработки заказов по id."""

        try:
            updated = await self._processor_settings_dao.update_endpoint_settings(
                session=self._session,
                setting_id=values.id,
                values=values.model_dump(),
            )
            if updated is None:
                raise HTTPException(
                    status_code=404,
                    detail=('Настройка не найдена по id. Используйте GET /processor/settings для списка валидных id.'),
                )
            return ProcessorSettingsResponseSchema.model_validate(updated)
        except IntegrityError:
            raise HTTPException(
                status_code=422,
                detail='Переданный status_mode_id или post_mode_id не существует.',
            ) from None

    async def get_status_mode_steps(self) -> list[ProcessorStatusModeStepsNamedResponseSchema]:
        """Вернуть все шаги статусов для всех режимов статусов."""

        settings = await self._processor_status_mode_steps_dao.find_all_status_mode_steps(
            session=self._session,
        )
        return [ProcessorStatusModeStepsNamedResponseSchema.model_validate(setting) for setting in settings]

    async def update_status_mode_steps(
        self,
        values: ProcessorStatusModeStepUpdateRequestSchema,
    ) -> ProcessorStatusModeStepsResponseSchema:
        """Обновить один шаг режима статусов по id."""

        updated = await self._processor_status_mode_steps_dao.update_status_mode_step(
            session=self._session,
            step_id=values.id,
            values=values.model_dump(),
        )
        if updated is None:
            raise HTTPException(status_code=404, detail='Шаг статуса не найден по id.')
        return ProcessorStatusModeStepsResponseSchema.model_validate(updated)

    async def get_status_modes(self) -> list[ProcessorStatusModesResponseSchema]:
        """Вернуть все режимы статусов."""

        settings = await self._processor_status_modes_dao.find_all_status_modes(session=self._session)
        return [ProcessorStatusModesResponseSchema.model_validate(setting) for setting in settings]

    async def get_post_modes(self) -> list[ProcessorPostModesResponseSchema]:
        """Вернуть все режимы мгновенного ответа submit."""

        settings = await self._processor_post_modes_dao.find_all_post_modes(session=self._session)
        return [ProcessorPostModesResponseSchema.model_validate(setting) for setting in settings]

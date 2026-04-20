from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.settings.schemas.requests.base_settings_request_schema import BaseSettingsUpdateRequestSchema
from app.api.settings.schemas.responses.setter_settings_response_schema import SetterSettingsResponseSchema
from app.db.dao.setter_dao.setter_settings_dao import SetterSettingsDao


class SetterSettingsService:
    """Сервис для просмотра и обновления настроек соединения витрины."""

    def __init__(self, setter_settings_dao: SetterSettingsDao, session: AsyncSession) -> None:
        self._setter_settings_dao = setter_settings_dao
        self._session = session

    async def get_settings(self) -> list[SetterSettingsResponseSchema]:
        """Вернуть все настройки эндпоинтов витрины."""
        settings = await self._setter_settings_dao.find_all_settings(session=self._session)
        return [SetterSettingsResponseSchema.model_validate(setting) for setting in settings]

    async def update_setter_setting(
        self,
        values: BaseSettingsUpdateRequestSchema,
    ) -> SetterSettingsResponseSchema:
        """Обновить настройку витрины по id."""
        update = await self._setter_settings_dao.update_endpoint_settings(
            session=self._session,
            setting_id=values.id,
            values=values.model_dump(),
        )

        if update is None:
            raise HTTPException(
                status_code=404,
                detail='Настройка не найдена по id. Используйте эндпоинт списка для получения доступных id.',
            )
        return SetterSettingsResponseSchema.model_validate(update)

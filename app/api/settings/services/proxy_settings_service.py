from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.settings.schemas.requests.base_settings_request_schema import BaseSettingsUpdateRequestSchema
from app.api.settings.schemas.responses.proxy_settings_response_schema import ProxySettingsResponseSchema
from app.db.dao.proxy_dao.proxy_settings_dao import ProxySettingsDao


class ProxySettingsService:
    """Сервис для эндпоинтов настроек загрузки товаров."""

    def __init__(self, proxy_settings_dao: ProxySettingsDao, session: AsyncSession) -> None:
        self._proxy_settings_dao = proxy_settings_dao
        self._session = session

    async def get_settings(self) -> list[ProxySettingsResponseSchema]:
        """Вернуть все настройки эндпоинтов загрузки товаров."""

        settings = await self._proxy_settings_dao.find_all_settings(session=self._session)
        return [ProxySettingsResponseSchema.model_validate(setting) for setting in settings]

    async def update_proxy_setting(
        self,
        values: BaseSettingsUpdateRequestSchema,
    ) -> ProxySettingsResponseSchema:
        """Обновить одну настройку эндпоинта загрузки товаров по id."""

        update = await self._proxy_settings_dao.update_endpoint_settings(
            session=self._session,
            setting_id=values.id,
            values=values.model_dump(),
        )

        if update is None:
            raise HTTPException(
                status_code=404,
                detail='Настройка загрузки товаров не найдена по id.',
            )

        return ProxySettingsResponseSchema.model_validate(update)

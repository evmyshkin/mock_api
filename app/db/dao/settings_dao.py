from collections.abc import Mapping
from enum import Enum
from typing import Any
from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dao.base_dao import BaseDAO
from app.db.models.base_models import BaseSettingsModel
from app.db.session import connection


class SettingsDao(BaseDAO):
    model: type[BaseSettingsModel]

    @connection
    async def get_endpoint_settings(self, session: AsyncSession, endpoint_type: Enum) -> BaseSettingsModel:
        """Найти настройки для ручки по endpoint_type."""
        settings = await self.find_one_or_none(session=session, endpoint_type=endpoint_type.value)
        if settings is None:
            raise ValueError(f'Не найдена настройка для ручки {endpoint_type.value}')
        return cast(BaseSettingsModel, settings)

    @connection
    async def find_all_settings(self, session: AsyncSession) -> list[BaseSettingsModel]:
        """Найти настройки для всех ручек."""
        settings = await self.find_all_ordered(session=session)
        return cast(list[BaseSettingsModel], settings)

    @connection
    async def update_endpoint_settings(
        self,
        session: AsyncSession,
        setting_id: int,
        values: Mapping[str, Any],
    ) -> BaseSettingsModel | None:
        """Обновить настройки эндпоинта по идентификатору."""
        updated = await self.update_one_or_none(
            session=session,
            filter_by={'id': setting_id},
            values=values,
        )
        return cast(BaseSettingsModel | None, updated)

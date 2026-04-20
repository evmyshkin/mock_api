from typing import Any

from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.common.schemas.info_response_schema import InfoResponseSchema
from app.api.setter.enums import SetterEntityTypeEnum
from app.api.setter.schemas.v1.setter_clear_response_schema import SetterClearResponseSchema
from app.api.settings.endpoint_types_enum import SetterEndpointTypesEnum
from app.api.settings.services.connection_emulation_service import ConnectionEmulationService
from app.db.dao.setter_dao.setter_request_dao import SetterRequestDao
from app.db.dao.setter_dao.setter_settings_dao import SetterSettingsDao


class SetterService:
    """Сервис прикладной логики для операций с данными тестовой витрины."""

    def __init__(
        self,
        setter_request_dao: SetterRequestDao,
        setter_settings_dao: SetterSettingsDao,
        session: AsyncSession,
    ) -> None:
        self._setter_request_dao = setter_request_dao
        self._setter_settings_dao = setter_settings_dao
        self._session = session

    @staticmethod
    def _resolve_settings_endpoint(entity_type: SetterEntityTypeEnum) -> SetterEndpointTypesEnum:
        if entity_type is SetterEntityTypeEnum.PRODUCTS:
            return SetterEndpointTypesEnum.GET_PRODUCTS
        msg = f'Неподдерживаемый тип сущности витрины: {entity_type}'
        raise ValueError(msg)

    async def set_data(self, entity_type: SetterEntityTypeEnum, request: Any) -> InfoResponseSchema:
        """Сохранить данные со строгой схемой валидации."""
        await self._setter_request_dao.add_entity_records(
            session=self._session,
            entity_type=entity_type,
            values=request,
            is_validated=True,
        )
        return InfoResponseSchema(info='Данные сохранены для сущности', context={'entity_type': entity_type.value})

    async def set_data_open(self, entity_type: SetterEntityTypeEnum, request: Any) -> InfoResponseSchema:
        """Сохранить данные по свободной схеме."""
        await self._setter_request_dao.add_entity_records(
            session=self._session,
            entity_type=entity_type,
            values=request,
            is_validated=False,
        )
        return InfoResponseSchema(
            info='Данные по свободной схеме сохранены для сущности',
            context={'entity_type': entity_type.value},
        )

    async def get_data(self, entity_type: SetterEntityTypeEnum, res_obj: Response) -> list[dict]:
        """Получить накопленные записи данных сущности с эмуляцией параметров ответа."""
        settings_endpoint = self._resolve_settings_endpoint(entity_type=entity_type)
        settings = await self._setter_settings_dao.get_endpoint_settings(
            session=self._session,
            endpoint_type=settings_endpoint,
        )
        await ConnectionEmulationService.apply_connection_settings(
            response_delay=settings.response_delay,
            response_code=settings.response_code,
            res_obj=res_obj,
            db_session=self._session,
        )
        return await self._setter_request_dao.find_entity_payloads(
            session=self._session,
            entity_type=entity_type,
        )

    async def clear_entity(self, entity_type: SetterEntityTypeEnum) -> SetterClearResponseSchema:
        """Полностью удалить все записи данных сущности."""
        result = await self._setter_request_dao.clear_entity_records(
            session=self._session,
            entity_type=entity_type,
        )
        deleted_count = result.rowcount or 0
        return SetterClearResponseSchema(info=f'Очищены записи {entity_type.value}', deleted_count=deleted_count)

    async def clear_all(self) -> SetterClearResponseSchema:
        """Полностью удалить все записи данных по всем сущностям."""
        result = await self._setter_request_dao.clear_all_records(session=self._session)
        deleted_count = result.rowcount or 0
        return SetterClearResponseSchema(info='Очищены все записи витрины', deleted_count=deleted_count)

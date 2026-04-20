from typing import Any

from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.setter.schemas.v1.setter_clear_response_schema import SetterClearResponseSchema
from app.api.settings.endpoint_types_enum import ProxyEndpointTypesEnum
from app.api.settings.services.connection_emulation_service import ConnectionEmulationService
from app.db.dao.proxy_dao.proxy_request_dao import ProxyRequestDao
from app.db.dao.proxy_dao.proxy_settings_dao import ProxySettingsDao
from app.db.models.proxy_schema.proxy_request_model import ProxyRequestModel

from ..schemas.responses.proxy_request_response_schema import ProxyRequestResponseSchema


class ProxyService:
    """Сервис для захвата запросов загрузки товаров."""

    endpoint_type = ProxyEndpointTypesEnum.CAPTURE

    def __init__(
        self,
        proxy_request_dao: ProxyRequestDao,
        proxy_settings_dao: ProxySettingsDao,
        session: AsyncSession,
    ) -> None:
        self._proxy_request_dao = proxy_request_dao
        self._proxy_settings_dao = proxy_settings_dao
        self._session = session

    @staticmethod
    def _to_response(record: ProxyRequestModel | dict[str, Any]) -> ProxyRequestResponseSchema:
        return ProxyRequestResponseSchema.model_validate(record)

    async def capture_request(
        self,
        request: Request,
        payload: dict[str, Any],
        request_id: str,
        res_obj: Response,
    ) -> ProxyRequestResponseSchema:
        """Сохранить метаданные запроса и данные по идентификатору request_id."""

        record = await self._proxy_request_dao.upsert_record(
            session=self._session,
            request_id=request_id,
            query_params=dict(request.query_params.items()),
            headers=dict(request.headers.items()),
            body=payload,
        )

        settings = await self._proxy_settings_dao.get_endpoint_settings(
            session=self._session,
            endpoint_type=self.endpoint_type,
        )

        await ConnectionEmulationService.apply_connection_settings(
            response_delay=settings.response_delay,
            response_code=settings.response_code,
            res_obj=res_obj,
            db_session=self._session,
        )

        return self._to_response(record)

    async def get_records(self) -> list[ProxyRequestResponseSchema]:
        """Вернуть сохраненные записи в порядке от новых к старым."""

        records = await self._proxy_request_dao.find_records(session=self._session)
        return [self._to_response(record) for record in records]

    async def get_record(self, request_id: str) -> ProxyRequestResponseSchema:
        """Вернуть сохраненную запись по идентификатору запроса."""

        record = await self._proxy_request_dao.find_record_by_request_id(
            session=self._session,
            request_id=request_id,
        )
        if record is None:
            raise HTTPException(status_code=404, detail='Запись загрузки товара не найдена по request_id')

        return self._to_response(record)

    async def clear_records(self) -> SetterClearResponseSchema:
        """Полностью удалить все сохраненные записи."""

        result = await self._proxy_request_dao.clear_all_records(session=self._session)
        deleted_count = result.rowcount or 0
        return SetterClearResponseSchema(info='Очищены записи загрузки товаров', deleted_count=deleted_count)

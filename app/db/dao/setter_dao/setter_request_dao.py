from datetime import UTC
from datetime import datetime
from datetime import timedelta
from typing import Any

from sqlalchemy import Result
from sqlalchemy import delete
from sqlalchemy import desc
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.setter.enums import SetterEntityTypeEnum
from app.db.dao.base_dao import BaseDAO
from app.db.models.setter_schema.setter_request_model import SetterRequestModel
from app.db.session import connection


class SetterRequestDao(BaseDAO):
    """DAO для операций над записями данных тестовой витрины."""

    model = SetterRequestModel

    @staticmethod
    def _serialize_payload(value: Any) -> dict[str, Any]:
        """Преобразовать элемент данных в JSON-совместимый словарь."""
        if isinstance(value, dict):
            return value
        if hasattr(value, 'model_dump'):
            return value.model_dump(exclude_unset=True, mode='json')
        msg = f'Неподдерживаемый тип элемента данных: {type(value)!r}'
        raise TypeError(msg)

    @connection
    async def add_entity_records(
        self,
        session: AsyncSession,
        entity_type: SetterEntityTypeEnum,
        values: Any,
        is_validated: bool,
    ) -> list[SetterRequestModel]:
        """Добавить записи данных для конкретного типа сущности."""
        objs = [
            SetterRequestModel(
                entity_type=entity_type.value,
                payload=self._serialize_payload(value),
                is_validated=is_validated,
            )
            for value in values.root
        ]

        session.add_all(objs)
        await session.commit()

        return objs

    @connection
    async def find_entity_payloads(
        self,
        session: AsyncSession,
        entity_type: SetterEntityTypeEnum,
    ) -> list[dict]:
        """Получить список сохраненных данных для конкретного типа сущности."""
        records = await self.find_all_ordered(session=session, entity_type=entity_type.value)
        return [record.payload for record in records]

    @connection
    async def find_all_requests(self, session: AsyncSession) -> list[SetterRequestModel]:
        """Получить все сохраненные записи витрины от новых к старым."""
        query = select(self.model).order_by(desc(self.model.created), desc(self.model.id))
        result = await session.execute(query)
        records = result.scalars().all()
        return list(records)

    @connection
    async def clear_entity_records(
        self,
        session: AsyncSession,
        entity_type: SetterEntityTypeEnum,
    ) -> Result[Any]:
        """Полностью удалить все записи для конкретного типа сущности."""
        query = delete(self.model).where(self.model.entity_type == entity_type.value)
        result = await session.execute(query)
        await session.commit()
        return result

    @connection
    async def clear_all_records(self, session: AsyncSession) -> Result[Any]:
        """Полностью удалить все записи витрины."""
        query = delete(self.model)
        result = await session.execute(query)
        await session.commit()
        return result

    @connection
    async def clear_old_requests(self, session: AsyncSession, time_delta: int) -> Result[Any]:
        """Удалить записи старше настроенного интервала ретенции."""
        cutoff = datetime.now(tz=UTC) - timedelta(hours=time_delta)
        return await self.clear_old_data(session=session, cutoff=cutoff)

from collections.abc import Sequence
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import cast

from sqlalchemy import Result
from sqlalchemy import delete
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dao.base_dao import BaseDAO
from app.db.models.proxy_schema.proxy_request_model import ProxyRequestModel
from app.db.session import connection


class ProxyRequestDao(BaseDAO):
    """DAO для записей сохраненных запросов загрузки товаров."""

    model = ProxyRequestModel

    @connection
    async def upsert_record(
        self,
        session: AsyncSession,
        request_id: str,
        query_params: dict[str, Any],
        headers: dict[str, Any],
        body: dict[str, Any],
    ) -> dict[str, Any]:
        """Вставить или обновить запись запроса по request_id."""

        stmt = (
            insert(self.model)
            .values(
                request_id=request_id,
                query_params=query_params,
                headers=headers,
                body=body,
            )
            .on_conflict_do_update(
                index_elements=[self.model.request_id],
                set_={
                    'query_params': query_params,
                    'headers': headers,
                    'body': body,
                    'updated': func.now(),
                },
            )
            .returning(
                self.model.request_id,
                self.model.query_params,
                self.model.headers,
                self.model.body,
                self.model.created,
                self.model.updated,
            )
        )

        result = await session.execute(stmt)
        row = result.mappings().one()
        await session.commit()
        return dict(row)

    @connection
    async def find_record_by_request_id(
        self,
        session: AsyncSession,
        request_id: str,
    ) -> ProxyRequestModel | None:
        """Найти одну сохраненную запись запроса по request_id."""
        record = await self.find_one_or_none(session=session, request_id=request_id)
        return cast(ProxyRequestModel | None, record)

    @connection
    async def find_records(
        self,
        session: AsyncSession,
    ) -> list[ProxyRequestModel]:
        """Вернуть сохраненные запросы в порядке от новых к старым."""

        query = select(self.model).order_by(desc(self.model.created), desc(self.model.id))
        result = await session.execute(query)
        records: Sequence[ProxyRequestModel] = result.scalars().all()
        return list(records)

    @connection
    async def clear_all_records(self, session: AsyncSession) -> Result[Any]:
        """Полностью удалить все сохраненные записи загрузки товаров."""
        query = delete(self.model)
        result = await session.execute(query)
        await session.commit()
        return result

    @connection
    async def clear_old_requests(self, session: AsyncSession, time_delta: int) -> Result[Any]:
        """Удалить записи старше настроенного окна ретенции."""
        cutoff = datetime.now(tz=UTC) - timedelta(hours=time_delta)
        return await self.clear_old_data(session=session, cutoff=cutoff)

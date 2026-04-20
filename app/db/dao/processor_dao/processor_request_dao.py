from datetime import UTC
from datetime import datetime
from datetime import timedelta
from typing import Any

from sqlalchemy import CursorResult
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dao.base_dao import BaseDAO
from app.db.models.processor_schema.processor_request_model import ProcessorRequestModel
from app.db.models.processor_schema.processor_status_mode_models import ProcessorStatusModeStepsModel
from app.db.schemas.insert.processor_request_insert_schema import ProcessorRequestInsertSchema
from app.db.session import connection


class ProcessorRequestDao(BaseDAO):
    """DAO для записей запросов обработки заказов."""

    model = ProcessorRequestModel

    @connection
    async def add_request(
        self,
        session: AsyncSession,
        values: ProcessorRequestInsertSchema,
    ) -> ProcessorRequestModel:
        """Вставить новую запись отправленного запроса заказа."""
        obj = ProcessorRequestModel(**values.model_dump(exclude_unset=True))
        session.add(obj)
        await session.commit()
        return obj

    @connection
    async def find_request_and_status(self, session: AsyncSession, request_id: str) -> Any | None:
        """Найти один запрос заказа с текущим активным шагом статуса."""

        query = (
            select(
                func.jsonb_build_object(
                    'request',
                    func.jsonb_build_object(*ProcessorRequestModel.jsonb_build_object()),
                    'status_mode_steps',
                    func.jsonb_build_object(*ProcessorStatusModeStepsModel.jsonb_build_object()),
                )
            )
            .join(
                ProcessorStatusModeStepsModel,
                ProcessorRequestModel.status_step_id == ProcessorStatusModeStepsModel.id,
            )
            .where(ProcessorRequestModel.request_id == request_id)
        )

        result = await session.execute(query)
        return result.scalar_one_or_none()

    @connection
    async def find_requests(self, session: AsyncSession) -> list[ProcessorRequestModel]:
        """Вернуть сохраненные запросы в порядке от новых к старым."""

        query = select(self.model).order_by(desc(self.model.created), desc(self.model.id))
        result = await session.execute(query)
        records = result.scalars().all()
        return list(records)

    @connection
    async def clear_old_requests(self, session: AsyncSession, time_delta: int) -> CursorResult:
        """Удалить записи запросов заказа старше настроенного окна ретенции."""
        cutoff = datetime.now(tz=UTC) - timedelta(hours=time_delta)
        return await self.clear_old_data(session=session, cutoff=cutoff)

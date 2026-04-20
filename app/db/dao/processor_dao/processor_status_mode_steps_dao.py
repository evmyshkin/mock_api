from collections.abc import Sequence
from typing import Any

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dao.base_dao import BaseDAO
from app.db.models.processor_schema.processor_status_mode_models import ProcessorStatusModesModel
from app.db.models.processor_schema.processor_status_mode_models import ProcessorStatusModeStepsModel
from app.db.session import connection


class ProcessorStatusModeStepsDao(BaseDAO):
    """DAO для шагов статусов внутри режимов обработки заказов."""

    model = ProcessorStatusModeStepsModel

    @connection
    async def find_all_status_mode_steps(self, session: AsyncSession) -> Sequence[Any]:
        """Вернуть все шаги статусов с человекочитаемым именем режима."""

        query = (
            select(
                func.jsonb_build_object(
                    *ProcessorStatusModeStepsModel.jsonb_build_object(),
                    'status_mode_name',
                    ProcessorStatusModesModel.name,
                )
            )
            .select_from(ProcessorStatusModeStepsModel)
            .join(
                ProcessorStatusModesModel,
                ProcessorStatusModeStepsModel.status_mode_id == ProcessorStatusModesModel.id,
            )
            .order_by(ProcessorStatusModeStepsModel.id)
        )

        result = await session.execute(query)
        return result.scalars().all()

    @connection
    async def update_status_mode_step(
        self,
        session: AsyncSession,
        step_id: int,
        values: dict[str, Any],
    ) -> ProcessorStatusModeStepsModel | None:
        """Обновить один шаг статуса по id."""
        return await self.update_one_or_none(
            session=session,
            filter_by={'id': step_id},
            values=values,
        )

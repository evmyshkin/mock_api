from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dao.base_dao import BaseDAO
from app.db.models.processor_schema.processor_status_mode_models import ProcessorStatusModesModel
from app.db.session import connection


class ProcessorStatusModesDao(BaseDAO):
    """DAO для режимов статусов обработки заказов."""

    model = ProcessorStatusModesModel

    @connection
    async def find_all_status_modes(self, session: AsyncSession) -> list[ProcessorStatusModesModel]:
        """Вернуть все настроенные режимы перехода статусов."""
        return await self.find_all_ordered(session=session)

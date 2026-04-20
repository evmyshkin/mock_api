from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dao.base_dao import BaseDAO
from app.db.models.processor_schema.processor_post_mode_model import ProcessorPostModesModel
from app.db.session import connection


class ProcessorPostModesDao(BaseDAO):
    """DAO для режимов POST-ответа обработки заказов."""

    model = ProcessorPostModesModel

    @connection
    async def find_all_post_modes(self, session: AsyncSession) -> list[ProcessorPostModesModel]:
        """Вернуть все настроенные режимы ответа submit."""
        return await self.find_all_ordered(session=session)

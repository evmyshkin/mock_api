from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config import config
from app.db.dao.setter_dao.setter_request_dao import SetterRequestDao


class SetterDataSchedulerService:
    """Фоновые задачи ретенции записей витрины."""

    def __init__(
        self,
        setter_request_dao: SetterRequestDao,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> None:
        self._setter_request_dao = setter_request_dao
        self._session_maker = session_maker

    async def clear_old_setter_data_task(self) -> None:
        """Удалить устаревшие записи витрины."""
        time_delta = config.scheduler.setter_data_max_age_hours

        async with self._session_maker() as session:
            result = await self._setter_request_dao.clear_old_requests(
                session=session,
                time_delta=time_delta,
            )
        logger.info(f'Удалено {result.rowcount} записей requests старше {time_delta} часов.')

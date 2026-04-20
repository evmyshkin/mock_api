from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config import config
from app.db.dao.proxy_dao.proxy_request_dao import ProxyRequestDao


class ProxyDataSchedulerService:
    """Фоновые задачи ретенции записей загрузки товаров."""

    def __init__(
        self,
        proxy_request_dao: ProxyRequestDao,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> None:
        self._proxy_request_dao = proxy_request_dao
        self._session_maker = session_maker

    async def clear_old_requests_task(self) -> None:
        """Удалить устаревшие записи загрузки товаров."""
        time_delta = config.scheduler.proxy_data_max_age_hours

        async with self._session_maker() as session:
            result = await self._proxy_request_dao.clear_old_requests(
                session=session,
                time_delta=time_delta,
            )

        logger.info(f'Удалено {result.rowcount} записей requests старше {time_delta} часов.')

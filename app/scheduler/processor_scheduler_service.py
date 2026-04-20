from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config import config
from app.db.dao.processor_dao.processor_request_dao import ProcessorRequestDao
from app.db.dao.processor_dao.processor_settings_dao import ProcessorSettingsDao


class ProcessorSchedulerService:
    """Фоновые задачи для машины состояний и ретенции обработки заказов."""

    def __init__(
        self,
        processor_request_dao: ProcessorRequestDao,
        processor_settings_dao: ProcessorSettingsDao,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> None:
        self._processor_request_dao = processor_request_dao
        self._processor_settings_dao = processor_settings_dao
        self._session_maker = session_maker

    async def order_status_change_task(self) -> None:
        """Продвинуть ожидающие статусы заказов согласно настроенным шагам режима статусов."""
        async with self._session_maker() as session:
            results = await self._processor_settings_dao.advance_status_steps(session=session)
        if len(results) > 0:
            logger.info(f'Обновления статусов обработки заказов: {results}')

    async def clear_old_requests_task(self) -> None:
        """Удалить старые записи запросов обработки заказов."""
        time_delta = config.scheduler.processor_data_max_age_hours

        async with self._session_maker() as session:
            result = await self._processor_request_dao.clear_old_requests(session=session, time_delta=time_delta)

        logger.info(f'Удалено {result.rowcount} записей requests старше {time_delta} часов.')

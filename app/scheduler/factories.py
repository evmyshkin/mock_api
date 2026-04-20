from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore

from app.db.dao.processor_dao.processor_request_dao import ProcessorRequestDao
from app.db.dao.processor_dao.processor_settings_dao import ProcessorSettingsDao
from app.db.dao.proxy_dao.proxy_request_dao import ProxyRequestDao
from app.db.dao.setter_dao.setter_request_dao import SetterRequestDao
from app.db.session import async_session_maker
from app.scheduler.processor_scheduler_service import ProcessorSchedulerService
from app.scheduler.proxy_data_scheduler_service import ProxyDataSchedulerService
from app.scheduler.setter_data_scheduler_service import SetterDataSchedulerService
from app.scheduler.start_main_scheduler import start_main_scheduler


def create_main_scheduler() -> AsyncIOScheduler:
    """Собрать планировщик с job-scoped зависимостями БД."""
    processor_scheduler_service = ProcessorSchedulerService(
        processor_request_dao=ProcessorRequestDao(),
        processor_settings_dao=ProcessorSettingsDao(),
        session_maker=async_session_maker,
    )
    setter_data_scheduler_service = SetterDataSchedulerService(
        setter_request_dao=SetterRequestDao(),
        session_maker=async_session_maker,
    )
    proxy_data_scheduler_service = ProxyDataSchedulerService(
        proxy_request_dao=ProxyRequestDao(),
        session_maker=async_session_maker,
    )
    return start_main_scheduler(
        processor_scheduler_service=processor_scheduler_service,
        setter_data_scheduler_service=setter_data_scheduler_service,
        proxy_data_scheduler_service=proxy_data_scheduler_service,
    )

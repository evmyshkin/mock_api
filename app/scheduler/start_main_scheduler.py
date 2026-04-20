from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore

from app.scheduler.processor_scheduler_service import ProcessorSchedulerService
from app.scheduler.proxy_data_scheduler_service import ProxyDataSchedulerService
from app.scheduler.setter_data_scheduler_service import SetterDataSchedulerService


def start_main_scheduler(
    processor_scheduler_service: ProcessorSchedulerService,
    setter_data_scheduler_service: SetterDataSchedulerService,
    proxy_data_scheduler_service: ProxyDataSchedulerService,
) -> AsyncIOScheduler:
    """Подготовить и запустить планировщик фоновых задач."""
    scheduler = AsyncIOScheduler()

    # Автопереход статусов обработки заказов (каждые 5 секунд)
    scheduler.add_job(processor_scheduler_service.order_status_change_task, 'cron', second='*/5')
    # Очистка старых запросов обработки заказов (ежедневно в 20:00)
    scheduler.add_job(processor_scheduler_service.clear_old_requests_task, 'cron', hour=20, minute=0)
    # Очистка старых данных Setter (ежедневно в 20:05)
    scheduler.add_job(setter_data_scheduler_service.clear_old_setter_data_task, 'cron', hour=20, minute=5)
    # Очистка старых записей загрузки товаров (ежедневно в 20:10)
    scheduler.add_job(
        proxy_data_scheduler_service.clear_old_requests_task,
        'cron',
        hour=20,
        minute=10,
    )
    scheduler.start()
    return scheduler

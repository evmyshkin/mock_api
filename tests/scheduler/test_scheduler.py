from unittest.mock import call

from app.scheduler.start_main_scheduler import start_main_scheduler


def test_start_main_scheduler_registers_expected_jobs(mocker):
    scheduler_mock = mocker.Mock()
    mocker.patch('app.scheduler.start_main_scheduler.AsyncIOScheduler', return_value=scheduler_mock)

    processor_scheduler_service = mocker.Mock(
        order_status_change_task=mocker.AsyncMock(),
        clear_old_requests_task=mocker.AsyncMock(),
    )
    setter_data_scheduler_service = mocker.Mock(
        clear_old_setter_data_task=mocker.AsyncMock(),
    )
    proxy_data_scheduler_service = mocker.Mock(
        clear_old_requests_task=mocker.AsyncMock(),
    )

    result = start_main_scheduler(
        processor_scheduler_service=processor_scheduler_service,
        setter_data_scheduler_service=setter_data_scheduler_service,
        proxy_data_scheduler_service=proxy_data_scheduler_service,
    )

    assert result is scheduler_mock
    scheduler_mock.add_job.assert_has_calls(
        [
            call(processor_scheduler_service.order_status_change_task, 'cron', second='*/5'),
            call(processor_scheduler_service.clear_old_requests_task, 'cron', hour=20, minute=0),
            call(setter_data_scheduler_service.clear_old_setter_data_task, 'cron', hour=20, minute=5),
            call(proxy_data_scheduler_service.clear_old_requests_task, 'cron', hour=20, minute=10),
        ]
    )
    scheduler_mock.start.assert_called_once_with()

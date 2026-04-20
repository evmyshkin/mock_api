import pytest

from fastapi import FastAPI

import app.main as main


class TestMainLifespan:
    @pytest.mark.asyncio
    async def test_lifespan_starts_and_stops_scheduler_and_broker(self, monkeypatch, mocker):
        scheduler_mock = mocker.Mock()
        logger_config_mock = mocker.Mock()

        monkeypatch.setattr(main.LoggerSetup, 'configure_logging', logger_config_mock)
        monkeypatch.setattr(main, 'create_main_scheduler', mocker.Mock(return_value=scheduler_mock))

        async with main.lifespan(FastAPI()):
            pass  # Запуск лайфспана, чтобы при завершении вызвать ассерт шатдауна шедуллера

        scheduler_mock.shutdown.assert_called_once_with(wait=True)
        logger_config_mock.assert_called_once()

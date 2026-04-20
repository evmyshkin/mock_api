import pytest

from app.api.setter.controllers import setter_data_controller


@pytest.mark.asyncio
class TestDataControllers:
    async def test_get_setter_data_returns_service_response(self, setter_data_response_list, mocker):
        service = mocker.Mock()
        service.get_setter_data = mocker.AsyncMock(return_value=setter_data_response_list)

        result = await setter_data_controller.get_setter_data(service=service)

        assert result == setter_data_response_list
        service.get_setter_data.assert_awaited_once_with()

    async def test_get_setter_data_reraises_service_error(self, mocker):
        service = mocker.Mock()
        service.get_setter_data = mocker.AsyncMock(side_effect=RuntimeError('сервис завершился с ошибкой'))

        with pytest.raises(RuntimeError, match='сервис завершился с ошибкой'):
            await setter_data_controller.get_setter_data(service=service)

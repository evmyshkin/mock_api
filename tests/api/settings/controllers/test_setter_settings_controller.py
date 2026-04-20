import pytest

from app.api.settings.controllers import setter_settings_controller


@pytest.mark.asyncio
class TestSetterSettingsController:
    async def test_get_settings_returns_service_response(self, setter_settings_response_list, mocker):
        service = mocker.Mock()
        service.get_settings = mocker.AsyncMock(return_value=setter_settings_response_list)

        result = await setter_settings_controller.get_settings(service=service)

        assert result == setter_settings_response_list
        service.get_settings.assert_awaited_once_with()

    async def test_update_setter_setting_returns_service_response(
        self,
        setter_settings_update_request,
        setter_settings_response,
        mocker,
    ):
        service = mocker.Mock()
        service.update_setter_setting = mocker.AsyncMock(return_value=setter_settings_response)

        result = await setter_settings_controller.update_setter_setting(
            request=setter_settings_update_request,
            service=service,
        )

        assert result == setter_settings_response
        service.update_setter_setting.assert_awaited_once_with(values=setter_settings_update_request)

    async def test_get_settings_reraises_service_error(self, mocker):
        service = mocker.Mock()
        service.get_settings = mocker.AsyncMock(side_effect=RuntimeError('сервис завершился с ошибкой'))

        with pytest.raises(RuntimeError, match='сервис завершился с ошибкой'):
            await setter_settings_controller.get_settings(service=service)

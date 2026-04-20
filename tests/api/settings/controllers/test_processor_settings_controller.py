import pytest

from app.api.settings.controllers import processor_settings_controller

GET_ORDER_PROCESSING_SETTINGS_CASES = [
    (
        'get_settings',
        'get_settings',
        'processor_settings_response_list',
    ),
    (
        'get_post_modes',
        'get_post_modes',
        'processor_post_modes_response_list',
    ),
    (
        'get_status_modes',
        'get_status_modes',
        'processor_status_modes_response_list',
    ),
    (
        'get_status_mode_steps',
        'get_status_mode_steps',
        'processor_status_mode_steps_named_response_list',
    ),
]


@pytest.mark.asyncio
class TestProcessorSettingsController:
    @pytest.mark.parametrize(
        ('controller_name', 'service_method_name', 'response_fixture'),
        GET_ORDER_PROCESSING_SETTINGS_CASES,
    )
    async def test_get_controllers_return_service_response(
        self,
        request,
        controller_name,
        service_method_name,
        response_fixture,
        mocker,
    ):
        service_response = request.getfixturevalue(response_fixture)
        service = mocker.Mock()
        setattr(service, service_method_name, mocker.AsyncMock(return_value=service_response))

        result = await getattr(processor_settings_controller, controller_name)(service=service)

        assert result == service_response
        getattr(service, service_method_name).assert_awaited_once_with()

    async def test_update_processor_setting_returns_service_response(
        self,
        processor_settings_update_request,
        processor_settings_response,
        mocker,
    ):
        service = mocker.Mock()
        service.update_processor_setting = mocker.AsyncMock(return_value=processor_settings_response)

        result = await processor_settings_controller.update_processor_setting(
            request=processor_settings_update_request,
            service=service,
        )

        assert result == processor_settings_response
        service.update_processor_setting.assert_awaited_once_with(values=processor_settings_update_request)

    async def test_update_status_mode_steps_returns_service_response(
        self,
        processor_status_mode_step_update_request,
        processor_status_mode_steps_response,
        mocker,
    ):
        service = mocker.Mock()
        service.update_status_mode_steps = mocker.AsyncMock(
            return_value=processor_status_mode_steps_response,
        )

        result = await processor_settings_controller.update_status_mode_steps(
            request=processor_status_mode_step_update_request,
            service=service,
        )

        assert result == processor_status_mode_steps_response
        service.update_status_mode_steps.assert_awaited_once_with(
            values=processor_status_mode_step_update_request,
        )

    async def test_get_settings_reraises_service_error(self, mocker):
        service = mocker.Mock()
        service.get_settings = mocker.AsyncMock(side_effect=RuntimeError('сервис завершился с ошибкой'))
        with pytest.raises(RuntimeError, match='сервис завершился с ошибкой'):
            await processor_settings_controller.get_settings(service=service)

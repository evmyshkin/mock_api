import pytest

from app.api.dependencies.settings_deps import get_processor_settings_service

GET_ORDER_PROCESSING_SETTINGS_API_CASES = [
    (
        '',
        'get_settings',
        'processor_settings_response_list',
    ),
    (
        '/post-modes',
        'get_post_modes',
        'processor_post_modes_response_list',
    ),
    (
        '/status-modes',
        'get_status_modes',
        'processor_status_modes_response_list',
    ),
    (
        '/status-mode-steps',
        'get_status_mode_steps',
        'processor_status_mode_steps_named_response_list',
    ),
]

PUT_ORDER_PROCESSING_SETTINGS_API_CASES = [
    (
        '',
        'update_processor_setting',
        'processor_settings_update_request',
        'processor_settings_response',
    ),
    (
        '/status-mode-steps',
        'update_status_mode_steps',
        'processor_status_mode_step_update_request',
        'processor_status_mode_steps_response',
    ),
]


@pytest.mark.asyncio
class TestProcessorSettingsControllerApi:
    @pytest.mark.parametrize(
        ('path_suffix', 'service_method_name', 'response_fixture'),
        GET_ORDER_PROCESSING_SETTINGS_API_CASES,
    )
    async def test_get_settings_endpoints(
        self,
        api_async_client,
        api_dependency_overrides,
        request,
        path_suffix,
        service_method_name,
        response_fixture,
        mocker,
    ):
        service_response = request.getfixturevalue(response_fixture)

        service = mocker.Mock()
        setattr(service, service_method_name, mocker.AsyncMock(return_value=service_response))
        api_dependency_overrides[get_processor_settings_service] = lambda: service
        res = await api_async_client.get(f'/processor/settings{path_suffix}')

        assert res.status_code == 200
        assert res.json() == [item.model_dump(mode='json', by_alias=True) for item in service_response]
        getattr(service, service_method_name).assert_awaited_once_with()

    @pytest.mark.parametrize(
        ('path_suffix', 'service_method_name', 'request_fixture', 'response_fixture'),
        PUT_ORDER_PROCESSING_SETTINGS_API_CASES,
    )
    async def test_put_settings_endpoints(
        self,
        api_async_client,
        api_dependency_overrides,
        request,
        path_suffix,
        service_method_name,
        request_fixture,
        response_fixture,
        mocker,
    ):
        payload = request.getfixturevalue(request_fixture)
        service_response = request.getfixturevalue(response_fixture)

        service = mocker.Mock()
        setattr(service, service_method_name, mocker.AsyncMock(return_value=service_response))
        api_dependency_overrides[get_processor_settings_service] = lambda: service
        res = await api_async_client.put(
            f'/processor/settings{path_suffix}',
            json=payload.model_dump(mode='json', by_alias=True),
        )

        assert res.status_code == 200
        assert res.json() == service_response.model_dump(mode='json', by_alias=True)

        sent_values = getattr(service, service_method_name).await_args.kwargs['values']
        assert sent_values.model_dump(mode='json', by_alias=True) == payload.model_dump(
            mode='json',
            by_alias=True,
        )

    @pytest.mark.parametrize(
        ('path_suffix', 'service_method_name'),
        [(case[0], case[1]) for case in PUT_ORDER_PROCESSING_SETTINGS_API_CASES],
    )
    async def test_put_settings_endpoints_return_422_on_invalid_payload(
        self,
        api_async_client,
        api_dependency_overrides,
        path_suffix,
        service_method_name,
        mocker,
    ):
        service = mocker.Mock()
        setattr(service, service_method_name, mocker.AsyncMock())
        api_dependency_overrides[get_processor_settings_service] = lambda: service
        res = await api_async_client.put(f'/processor/settings{path_suffix}', json={})

        assert res.status_code == 422
        getattr(service, service_method_name).assert_not_awaited()

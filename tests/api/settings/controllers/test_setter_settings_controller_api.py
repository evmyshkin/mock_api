import pytest

from app.api.dependencies.settings_deps import get_setter_settings_service


@pytest.mark.asyncio
class TestSetterSettingsControllerApi:
    async def test_get_settings_endpoint(
        self,
        api_async_client,
        api_dependency_overrides,
        setter_settings_response_list,
        mocker,
    ):
        service = mocker.Mock()
        service.get_settings = mocker.AsyncMock(return_value=setter_settings_response_list)
        api_dependency_overrides[get_setter_settings_service] = lambda: service

        res = await api_async_client.get('/setter/settings')

        assert res.status_code == 200
        assert res.json() == [item.model_dump(mode='json', by_alias=True) for item in setter_settings_response_list]
        service.get_settings.assert_awaited_once_with()

    async def test_put_settings_endpoint(
        self,
        api_async_client,
        api_dependency_overrides,
        setter_settings_update_request,
        setter_settings_response,
        mocker,
    ):
        service = mocker.Mock()
        service.update_setter_setting = mocker.AsyncMock(return_value=setter_settings_response)
        api_dependency_overrides[get_setter_settings_service] = lambda: service

        res = await api_async_client.put(
            '/setter/settings',
            json=setter_settings_update_request.model_dump(mode='json', by_alias=True),
        )

        assert res.status_code == 200
        assert res.json() == setter_settings_response.model_dump(mode='json', by_alias=True)
        sent_values = service.update_setter_setting.await_args.kwargs['values']
        assert sent_values.model_dump(mode='json', by_alias=True) == setter_settings_update_request.model_dump(
            mode='json',
            by_alias=True,
        )

    async def test_put_settings_endpoint_returns_422_on_invalid_payload(
        self,
        api_async_client,
        api_dependency_overrides,
        mocker,
    ):
        service = mocker.Mock()
        service.update_setter_setting = mocker.AsyncMock()
        api_dependency_overrides[get_setter_settings_service] = lambda: service

        res = await api_async_client.put('/setter/settings', json={})

        assert res.status_code == 422
        service.update_setter_setting.assert_not_awaited()

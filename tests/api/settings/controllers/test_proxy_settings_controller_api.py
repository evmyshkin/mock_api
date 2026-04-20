import pytest

from app.api.dependencies.settings_deps import get_proxy_settings_service


@pytest.mark.asyncio
class TestProxySettingsControllerApi:
    async def test_get_settings_endpoint(
        self,
        api_async_client,
        api_dependency_overrides,
        proxy_settings_response_list,
        mocker,
    ):
        service = mocker.Mock()
        service.get_settings = mocker.AsyncMock(return_value=proxy_settings_response_list)
        api_dependency_overrides[get_proxy_settings_service] = lambda: service

        res = await api_async_client.get('/proxy/settings')

        assert res.status_code == 200
        assert res.json() == [item.model_dump(mode='json', by_alias=True) for item in proxy_settings_response_list]
        service.get_settings.assert_awaited_once_with()

    async def test_put_settings_endpoint(
        self,
        api_async_client,
        api_dependency_overrides,
        proxy_settings_update_request,
        proxy_settings_response,
        mocker,
    ):
        service = mocker.Mock()
        service.update_proxy_setting = mocker.AsyncMock(return_value=proxy_settings_response)
        api_dependency_overrides[get_proxy_settings_service] = lambda: service

        res = await api_async_client.put(
            '/proxy/settings',
            json=proxy_settings_update_request.model_dump(mode='json', by_alias=True),
        )

        assert res.status_code == 200
        assert res.json() == proxy_settings_response.model_dump(mode='json', by_alias=True)
        sent_values = service.update_proxy_setting.await_args.kwargs['values']
        assert sent_values.model_dump(mode='json', by_alias=True) == proxy_settings_update_request.model_dump(
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
        service.update_proxy_setting = mocker.AsyncMock()
        api_dependency_overrides[get_proxy_settings_service] = lambda: service

        res = await api_async_client.put('/proxy/settings', json={})

        assert res.status_code == 422
        service.update_proxy_setting.assert_not_awaited()

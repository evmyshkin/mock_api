import pytest

from app.api.dependencies.setter_data_deps import get_setter_data_service


@pytest.mark.asyncio
class TestDataControllersApi:
    async def test_get_setter_data_endpoint(
        self,
        api_async_client,
        api_dependency_overrides,
        setter_data_response_list,
        mocker,
    ):
        service = mocker.Mock()
        service.get_setter_data = mocker.AsyncMock(return_value=setter_data_response_list)
        api_dependency_overrides[get_setter_data_service] = lambda: service

        res = await api_async_client.get('/setter/api/v1/requests')

        assert res.status_code == 200
        assert res.json() == [item.model_dump(mode='json', by_alias=True) for item in setter_data_response_list]
        service.get_setter_data.assert_awaited_once_with()

    async def test_legacy_data_url_is_unavailable(self, api_async_client):
        res = await api_async_client.get('/setter/data/requests')
        assert res.status_code == 404

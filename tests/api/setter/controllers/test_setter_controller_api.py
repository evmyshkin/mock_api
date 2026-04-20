import pytest

from fastapi import Response

from app.api.dependencies.setter_deps import get_setter_service


@pytest.mark.asyncio
class TestSetterControllerApi:
    async def test_products_set_and_get_and_clear_flow(
        self,
        api_async_client,
        api_dependency_overrides,
        product_strict_request,
        mocker,
    ):
        service = mocker.Mock()
        service.set_data = mocker.AsyncMock(return_value={'info': 'ok', 'context': {'entity_type': 'products'}})
        service.set_data_open = mocker.AsyncMock(return_value={'info': 'ok', 'context': {'entity_type': 'products'}})
        service.get_data = mocker.AsyncMock(return_value=[product_strict_request.root[0].model_dump(mode='json')])
        service.clear_entity = mocker.AsyncMock(return_value={'info': 'cleared', 'deleted_count': 1})
        service.clear_all = mocker.AsyncMock(return_value={'info': 'cleared all', 'deleted_count': 1})
        api_dependency_overrides[get_setter_service] = lambda: service

        set_res = await api_async_client.post(
            '/setter/api/v1/products/set', json=product_strict_request.model_dump(mode='json')
        )
        assert set_res.status_code == 200

        get_res = await api_async_client.get('/setter/api/v1/products')
        assert get_res.status_code == 200
        assert len(get_res.json()['items']) == 1
        assert service.get_data.await_args.kwargs['entity_type'].value == 'products'
        assert isinstance(service.get_data.await_args.kwargs['res_obj'], Response)

        clear_res = await api_async_client.delete('/setter/api/v1/products')
        assert clear_res.status_code == 200
        assert clear_res.json()['deleted_count'] == 1

        clear_all_res = await api_async_client.delete('/setter/api/v1/clear')
        assert clear_all_res.status_code == 200
        assert clear_all_res.json()['deleted_count'] == 1

    async def test_products_set_returns_422_on_invalid_payload(
        self,
        api_async_client,
        api_dependency_overrides,
        mocker,
    ):
        service = mocker.Mock()
        service.set_data = mocker.AsyncMock()
        api_dependency_overrides[get_setter_service] = lambda: service

        # отсутствуют обязательные поля
        res = await api_async_client.post('/setter/api/v1/products/set', json={'root': [{'name': 'x'}]})

        assert res.status_code == 422
        service.set_data.assert_not_awaited()

    async def test_products_set_open_accepts_extra_fields(
        self,
        api_async_client,
        api_dependency_overrides,
        product_open_request,
        mocker,
    ):
        service = mocker.Mock()
        service.set_data_open = mocker.AsyncMock(return_value={'info': 'ok', 'context': {'entity_type': 'products'}})
        api_dependency_overrides[get_setter_service] = lambda: service

        res = await api_async_client.post(
            '/setter/api/v1/products/set-open', json=product_open_request.model_dump(mode='json')
        )

        assert res.status_code == 200
        sent_request = service.set_data_open.await_args.kwargs['request']
        assert sent_request.root[0]['color'] == 'black'

    async def test_products_set_rejects_empty_root(self, api_async_client, api_dependency_overrides, mocker):
        service = mocker.Mock()
        service.set_data = mocker.AsyncMock()
        api_dependency_overrides[get_setter_service] = lambda: service

        res = await api_async_client.post('/setter/api/v1/products/set', json={'root': []})

        assert res.status_code == 422
        service.set_data.assert_not_awaited()

    async def test_products_set_open_rejects_empty_root(self, api_async_client, api_dependency_overrides, mocker):
        service = mocker.Mock()
        service.set_data_open = mocker.AsyncMock()
        api_dependency_overrides[get_setter_service] = lambda: service

        res = await api_async_client.post('/setter/api/v1/products/set-open', json={'root': []})

        assert res.status_code == 422
        service.set_data_open.assert_not_awaited()

    async def test_orders_and_customers_routes_are_unavailable(self, api_async_client):
        orders_res = await api_async_client.get('/api/v1/orders')
        customers_res = await api_async_client.get('/api/v1/customers')
        assert orders_res.status_code == 404
        assert customers_res.status_code == 404

    async def test_legacy_setter_routes_are_unavailable(self, api_async_client):
        res = await api_async_client.get('/v1/order/updated')
        assert res.status_code == 404

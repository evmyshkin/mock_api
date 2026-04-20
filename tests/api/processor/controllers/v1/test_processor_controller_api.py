import pytest

from fastapi import Response

from app.api.dependencies.processor_service_deps import get_processor_service


@pytest.mark.asyncio
class TestProcessorControllerApi:
    async def test_submit_endpoint(
        self,
        api_async_client,
        api_dependency_overrides,
        order_submit_request,
        order_submit_response,
        mocker,
    ):
        service = mocker.Mock()
        service.submit_order = mocker.AsyncMock(return_value=order_submit_response)
        api_dependency_overrides[get_processor_service] = lambda: service

        res = await api_async_client.post(
            '/processor/api/v1/order',
            json=order_submit_request.model_dump(mode='json', by_alias=True),
        )

        assert res.status_code == 200
        assert res.json() == order_submit_response.model_dump(mode='json', by_alias=True, exclude_none=True)

        sent_request = service.submit_order.await_args.kwargs['request']
        assert sent_request.model_dump(mode='json', by_alias=True) == order_submit_request.model_dump(
            mode='json',
            by_alias=True,
        )
        assert isinstance(service.submit_order.await_args.kwargs['res_obj'], Response)

    async def test_submit_endpoint_returns_422_on_invalid_payload(
        self,
        api_async_client,
        api_dependency_overrides,
        mocker,
    ):
        service = mocker.Mock()
        service.submit_order = mocker.AsyncMock()
        api_dependency_overrides[get_processor_service] = lambda: service

        res = await api_async_client.post('/processor/api/v1/order', json={})

        assert res.status_code == 422
        service.submit_order.assert_not_awaited()

    async def test_status_endpoint(
        self,
        api_async_client,
        api_dependency_overrides,
        order_status_response,
        mocker,
    ):
        service = mocker.Mock()
        service.get_order_status = mocker.AsyncMock(return_value=order_status_response)
        api_dependency_overrides[get_processor_service] = lambda: service

        res = await api_async_client.get('/processor/api/v1/status', params={'request_id': 'req-1'})

        assert res.status_code == 200
        assert res.json() == order_status_response.model_dump(mode='json', by_alias=True, exclude_none=True)
        assert service.get_order_status.await_args.kwargs['request_id'] == 'req-1'
        assert isinstance(service.get_order_status.await_args.kwargs['res_obj'], Response)

    async def test_status_endpoint_returns_422_without_request_id(
        self,
        api_async_client,
        api_dependency_overrides,
        mocker,
    ):
        service = mocker.Mock()
        service.get_order_status = mocker.AsyncMock()
        api_dependency_overrides[get_processor_service] = lambda: service

        res = await api_async_client.get('/processor/api/v1/status')

        assert res.status_code == 422
        service.get_order_status.assert_not_awaited()

    async def test_requests_endpoint(
        self,
        api_async_client,
        api_dependency_overrides,
        order_request_response,
        mocker,
    ):
        service = mocker.Mock()
        service.get_requests = mocker.AsyncMock(return_value=[order_request_response])
        api_dependency_overrides[get_processor_service] = lambda: service

        res = await api_async_client.get('/processor/api/v1/requests')

        assert res.status_code == 200
        assert res.json() == [order_request_response.model_dump(mode='json', by_alias=True)]
        service.get_requests.assert_awaited_once_with()

    async def test_legacy_processor_routes_are_unavailable(self, api_async_client):
        res = await api_async_client.get('/api/v7/status', params={'request_id': 'req-1'})
        assert res.status_code == 404

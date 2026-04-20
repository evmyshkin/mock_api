from datetime import UTC
from datetime import datetime

import pytest

from app.api.dependencies.proxy_deps import get_proxy_service
from app.api.proxy.schemas.responses.proxy_request_response_schema import ProxyRequestResponseSchema


def _record(request_id: str) -> ProxyRequestResponseSchema:
    dt = datetime(2026, 4, 18, 12, 0, 0, tzinfo=UTC)
    return ProxyRequestResponseSchema(
        request_id=request_id,
        query_params={'trace_id': 'abc123'},
        headers={'request_id': request_id},
        body={'url': 'https://s3.example.com/file.xlsx'},
        created=dt,
        updated=dt,
    )


@pytest.mark.asyncio
class TestProxyController:
    async def test_post_proxy_returns_service_payload(
        self,
        api_async_client,
        api_dependency_overrides,
        fixed_upload_payload,
        random_request_id,
        fixed_auth_header,
        mocker,
    ):
        expected = _record(request_id=random_request_id)
        service = mocker.Mock()
        service.capture_request = mocker.AsyncMock(return_value=expected)
        api_dependency_overrides[get_proxy_service] = lambda: service

        response = await api_async_client.post(
            url='/proxy/api/v1/pay',
            json=fixed_upload_payload,
            headers={'request_id': random_request_id, 'Authorization': fixed_auth_header},
        )

        assert response.status_code == 200
        assert response.json()['request_id'] == random_request_id
        assert response.json()['body'] == fixed_upload_payload
        service.capture_request.assert_awaited_once()
        sent_values = service.capture_request.await_args.kwargs
        assert sent_values['request_id'] == random_request_id
        assert sent_values['payload'] == fixed_upload_payload

    async def test_get_records_returns_service_payload(
        self,
        api_async_client,
        api_dependency_overrides,
        mocker,
    ):
        records = [_record(request_id='req-1')]
        service = mocker.Mock()
        service.get_records = mocker.AsyncMock(return_value=records)
        api_dependency_overrides[get_proxy_service] = lambda: service

        response = await api_async_client.get('/proxy/api/v1/requests')

        assert response.status_code == 200
        assert response.json()[0]['request_id'] == 'req-1'
        service.get_records.assert_awaited_once_with()

    async def test_get_record_returns_service_payload(
        self,
        api_async_client,
        api_dependency_overrides,
        mocker,
    ):
        service = mocker.Mock()
        service.get_record = mocker.AsyncMock(return_value=_record(request_id='req-1'))
        api_dependency_overrides[get_proxy_service] = lambda: service

        response = await api_async_client.get('/proxy/api/v1/requests/req-1')

        assert response.status_code == 200
        assert response.json()['request_id'] == 'req-1'
        service.get_record.assert_awaited_once_with(request_id='req-1')

    async def test_delete_records_returns_service_payload(
        self,
        api_async_client,
        api_dependency_overrides,
        mocker,
    ):
        service = mocker.Mock()
        service.clear_records = mocker.AsyncMock(return_value={'info': 'cleared', 'deleted_count': 2})
        api_dependency_overrides[get_proxy_service] = lambda: service

        response = await api_async_client.delete('/proxy/api/v1/requests')

        assert response.status_code == 200
        assert response.json() == {'info': 'cleared', 'deleted_count': 2}
        service.clear_records.assert_awaited_once_with()

    async def test_missing_request_id_returns_422(
        self,
        api_async_client,
        api_dependency_overrides,
        fixed_upload_payload,
        fixed_auth_header,
        mocker,
    ):
        service = mocker.Mock()
        service.capture_request = mocker.AsyncMock()
        api_dependency_overrides[get_proxy_service] = lambda: service

        response = await api_async_client.post(
            url='/proxy/api/v1/pay',
            json=fixed_upload_payload,
            headers={'Authorization': fixed_auth_header},
        )

        assert response.status_code == 422
        assert response.json()['detail'][0]['type'] == 'missing'
        assert response.json()['detail'][0]['loc'][1] == 'request_id'
        service.capture_request.assert_not_awaited()

    async def test_legacy_route_is_unavailable(self, api_async_client):
        response = await api_async_client.get('/api/middleware/v1/recorded_upload')
        assert response.status_code == 404

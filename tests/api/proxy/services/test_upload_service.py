from datetime import UTC
from datetime import datetime
from types import SimpleNamespace

import pytest

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response

from app.api.proxy.services.proxy_service import ProxyService
from app.api.settings.endpoint_types_enum import ProxyEndpointTypesEnum


def _build_request_with_headers_and_query() -> Request:
    scope = {
        'type': 'http',
        'method': 'POST',
        'path': '/proxy/api/v1/pay',
        'query_string': b'trace_id=abc123',
        'headers': [(b'request_id', b'req-1'), (b'authorization', b'Bearer 123')],
    }
    return Request(scope)


def _record(request_id: str = 'req-1') -> SimpleNamespace:
    dt = datetime(2026, 4, 18, 12, 0, 0, tzinfo=UTC)
    return SimpleNamespace(
        id=1,
        request_id=request_id,
        query_params={'trace_id': 'abc123'},
        headers={'request_id': request_id, 'authorization': 'Bearer 123'},
        body={'url': 'https://s3.example.com/file.xlsx'},
        created=dt,
        updated=dt,
    )


@pytest.mark.asyncio
class TestProxyService:
    async def test_capture_request_upserts_record_and_applies_settings(self, mocker):
        request = _build_request_with_headers_and_query()
        response = Response()

        session = mocker.Mock()
        settings = mocker.Mock(response_delay=3, response_code=202)
        proxy_settings_dao = mocker.Mock()
        proxy_settings_dao.get_endpoint_settings = mocker.AsyncMock(return_value=settings)

        proxy_request_dao = mocker.Mock()
        proxy_request_dao.upsert_record = mocker.AsyncMock(return_value=_record())

        apply_connection_settings_mock = mocker.patch(
            'app.api.proxy.services.proxy_service.ConnectionEmulationService.apply_connection_settings',
            new=mocker.AsyncMock(),
        )

        service = ProxyService(
            proxy_request_dao=proxy_request_dao,
            proxy_settings_dao=proxy_settings_dao,
            session=session,
        )

        result = await service.capture_request(
            request=request,
            payload={'url': 'https://s3.example.com/file.xlsx'},
            request_id='req-1',
            res_obj=response,
        )

        assert result.request_id == 'req-1'
        assert result.body == {'url': 'https://s3.example.com/file.xlsx'}
        proxy_request_dao.upsert_record.assert_awaited_once_with(
            session=session,
            request_id='req-1',
            query_params={'trace_id': 'abc123'},
            headers={'request_id': 'req-1', 'authorization': 'Bearer 123'},
            body={'url': 'https://s3.example.com/file.xlsx'},
        )
        proxy_settings_dao.get_endpoint_settings.assert_awaited_once_with(
            session=session,
            endpoint_type=ProxyEndpointTypesEnum.CAPTURE,
        )
        apply_connection_settings_mock.assert_awaited_once_with(
            res_obj=response,
            response_delay=3,
            response_code=202,
            db_session=session,
        )

    async def test_get_records_returns_response_list(self, mocker):
        session = mocker.Mock()
        proxy_request_dao = mocker.Mock()
        proxy_request_dao.find_records = mocker.AsyncMock(return_value=[_record('req-1'), _record('req-2')])
        proxy_settings_dao = mocker.Mock()

        service = ProxyService(
            proxy_request_dao=proxy_request_dao,
            proxy_settings_dao=proxy_settings_dao,
            session=session,
        )

        result = await service.get_records()

        assert len(result) == 2
        assert result[0].request_id == 'req-1'
        proxy_request_dao.find_records.assert_awaited_once_with(session=session)

    async def test_get_record_raises_404_when_missing(self, mocker):
        session = mocker.Mock()
        proxy_request_dao = mocker.Mock()
        proxy_request_dao.find_record_by_request_id = mocker.AsyncMock(return_value=None)
        proxy_settings_dao = mocker.Mock()

        service = ProxyService(
            proxy_request_dao=proxy_request_dao,
            proxy_settings_dao=proxy_settings_dao,
            session=session,
        )

        with pytest.raises(HTTPException) as exc:
            await service.get_record(request_id='req-missing')

        assert exc.value.status_code == 404

    async def test_clear_records_returns_deleted_count(self, mocker):
        session = mocker.Mock()
        proxy_request_dao = mocker.Mock()
        proxy_request_dao.clear_all_records = mocker.AsyncMock(return_value=SimpleNamespace(rowcount=3))
        proxy_settings_dao = mocker.Mock()

        service = ProxyService(
            proxy_request_dao=proxy_request_dao,
            proxy_settings_dao=proxy_settings_dao,
            session=session,
        )

        result = await service.clear_records()

        assert result.deleted_count == 3
        assert result.info == 'Очищены записи загрузки товаров'
        proxy_request_dao.clear_all_records.assert_awaited_once_with(session=session)

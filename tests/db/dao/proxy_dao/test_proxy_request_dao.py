from datetime import UTC
from datetime import datetime
from types import SimpleNamespace

import pytest

from app.db.dao.proxy_dao.proxy_request_dao import ProxyRequestDao


@pytest.fixture
def proxy_request_dao() -> ProxyRequestDao:
    return ProxyRequestDao()


@pytest.mark.asyncio
class TestProxyRequestDao:
    async def test_find_record_by_request_id_proxies_to_find_one_or_none(self, proxy_request_dao, mocker):
        expected = object()
        find_one_mock = mocker.patch.object(proxy_request_dao, 'find_one_or_none', return_value=expected)

        result = await proxy_request_dao.find_record_by_request_id(request_id='req-1')

        assert result is expected
        find_one_mock.assert_awaited_once_with(session=mocker.ANY, request_id='req-1')

    async def test_clear_all_records_executes_delete(self, fake_session, proxy_request_dao):
        fake_session.execute.return_value = SimpleNamespace(rowcount=5)

        result = await proxy_request_dao.clear_all_records(session=fake_session)

        assert result.rowcount == 5
        fake_session.execute.assert_awaited_once()
        statement = str(fake_session.execute.await_args.args[0])
        assert 'DELETE FROM proxy_schema.requests' in statement

    async def test_clear_old_requests_delegates_to_clear_old_data(self, proxy_request_dao, mocker):
        expected = object()
        clear_old_data_mock = mocker.patch.object(proxy_request_dao, 'clear_old_data', return_value=expected)

        result = await proxy_request_dao.clear_old_requests(time_delta=24)

        assert result is expected
        clear_old_data_mock.assert_awaited_once()
        cutoff = clear_old_data_mock.await_args.kwargs['cutoff']
        assert isinstance(cutoff, datetime)
        assert cutoff.tzinfo is UTC

    async def test_find_records_orders_by_created_desc(self, proxy_request_dao, mocker):
        scalars = mocker.Mock()
        scalars.all.return_value = [SimpleNamespace(request_id='req-1')]
        execute_result = mocker.Mock(scalars=mocker.Mock(return_value=scalars))

        session = mocker.Mock()
        session.execute = mocker.AsyncMock(return_value=execute_result)

        result = await proxy_request_dao.find_records(session=session)

        assert len(result) == 1
        assert result[0].request_id == 'req-1'
        session.execute.assert_awaited_once()

    async def test_upsert_record_commits_and_returns_row(self, proxy_request_dao, mocker):
        expected = {
            'request_id': 'req-1',
            'query_params': {'trace_id': 'abc'},
            'headers': {'request_id': 'req-1'},
            'body': {'url': 'https://s3.example.com/file.xlsx'},
            'created': datetime(2026, 4, 18, 12, 0, 0, tzinfo=UTC),
            'updated': datetime(2026, 4, 18, 12, 0, 0, tzinfo=UTC),
        }
        mappings_result = mocker.Mock(one=mocker.Mock(return_value=expected))
        execute_result = mocker.Mock(mappings=mocker.Mock(return_value=mappings_result))

        session = mocker.Mock()
        session.execute = mocker.AsyncMock(return_value=execute_result)
        session.commit = mocker.AsyncMock()

        result = await proxy_request_dao.upsert_record(
            session=session,
            request_id='req-1',
            query_params={'trace_id': 'abc'},
            headers={'request_id': 'req-1'},
            body={'url': 'https://s3.example.com/file.xlsx'},
        )

        assert result == expected
        session.execute.assert_awaited_once()
        session.commit.assert_awaited_once_with()

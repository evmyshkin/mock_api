from datetime import UTC
from datetime import datetime

import pytest

from app.api.settings.endpoint_types_enum import ProcessorEndpointTypesEnum
from app.db.dao.processor_dao.processor_request_dao import ProcessorRequestDao
from app.db.schemas.insert.processor_request_insert_schema import ProcessorRequestInsertSchema


@pytest.fixture
def processor_request_dao() -> ProcessorRequestDao:
    return ProcessorRequestDao()


@pytest.mark.asyncio
class TestProcessorRequestDao:
    async def test_add_request_creates_and_returns_model(self, fake_session, processor_request_dao):
        values = ProcessorRequestInsertSchema(
            request_id='request-1',
            endpoint_type=ProcessorEndpointTypesEnum.SUBMIT,
            order_id='order-1',
            customer_id='customer-1',
            post_mode_id=1,
            status_mode_id=1,
            status_step_id=1,
            unixtimestamp=1710000000,
            response_code=200,
            response_delay=0,
            status_change_after=None,
            payload={'order_id': 'order-1'},
        )

        result = await processor_request_dao.add_request(values=values)

        assert result.request_id == 'request-1'
        assert result.endpoint_type == ProcessorEndpointTypesEnum.SUBMIT.value
        assert result.order_id == 'order-1'
        assert result.customer_id == 'customer-1'
        assert result.payload == {'order_id': 'order-1'}
        fake_session.add.assert_called_once()
        fake_session.commit.assert_awaited_once_with()

    async def test_find_request_and_status_returns_row(self, fake_session, processor_request_dao, mocker):
        expected = {'request': {'request_id': 'request-1'}}
        execute_result = mocker.MagicMock()
        execute_result.scalar_one_or_none.return_value = expected
        fake_session.execute.return_value = execute_result

        result = await processor_request_dao.find_request_and_status(request_id='request-1')

        assert result == expected
        fake_session.execute.assert_awaited_once()

    async def test_find_requests_returns_rows(self, fake_session, processor_request_dao, mocker):
        expected = [mocker.Mock(request_id='request-2'), mocker.Mock(request_id='request-1')]
        execute_result = mocker.Mock()
        execute_result.scalars.return_value.all.return_value = expected
        fake_session.execute.return_value = execute_result

        result = await processor_request_dao.find_requests()

        assert result == expected
        fake_session.execute.assert_awaited_once()

    async def test_clear_old_requests_calls_clear_old_data_with_cutoff(self, processor_request_dao, mocker):
        expected = object()
        clear_old_data_mock = mocker.patch.object(processor_request_dao, 'clear_old_data', return_value=expected)

        result = await processor_request_dao.clear_old_requests(time_delta=3)

        assert result is expected
        clear_old_data_mock.assert_awaited_once()
        cutoff = clear_old_data_mock.await_args.kwargs['cutoff']
        assert isinstance(cutoff, datetime)
        assert cutoff.tzinfo == UTC

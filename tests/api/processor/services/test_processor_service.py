from types import SimpleNamespace

import pytest

from fastapi import HTTPException
from fastapi import Response

from app.api.processor.schemas.requests.processor_submit_request_schema import OrderLineItemSchema
from app.api.processor.schemas.requests.processor_submit_request_schema import ProcessorSubmitRequestSchema
from app.api.processor.services.processor_service import ProcessorService
from app.api.processor.utils.processor_exceptions import ProcessorSubmitError


@pytest.mark.asyncio
class TestProcessorService:
    @staticmethod
    def _build_full_config(post_error: dict | None = None):
        return SimpleNamespace(
            settings=SimpleNamespace(response_delay=2, response_code=202),
            post_modes=SimpleNamespace(id=1, error_message=post_error),
            status_modes=SimpleNamespace(id=1),
            status_mode_steps=SimpleNamespace(
                id=11,
                step_order=1,
                status='Заказ получен',
                duration=5,
                error_message=None,
            ),
            status_mode_len=3,
        )

    async def test_submit_order_applies_settings_and_persists_request(self, mocker):
        processor_request_dao = mocker.Mock()
        processor_request_dao.add_request = mocker.AsyncMock()

        processor_settings_dao = mocker.Mock()
        processor_settings_dao.get_endpoint_full_config = mocker.AsyncMock(
            return_value=self._build_full_config(post_error=None),
        )

        apply_connection_settings_mock = mocker.patch(
            'app.api.processor.services.processor_service.ConnectionEmulationService.apply_connection_settings',
            new=mocker.AsyncMock(),
        )

        session = mocker.Mock()
        service = ProcessorService(
            processor_request_dao=processor_request_dao,
            processor_settings_dao=processor_settings_dao,
            session=session,
        )
        response = Response()
        request = ProcessorSubmitRequestSchema(
            order_id='order-1',
            customer_id='customer-1',
            items=[OrderLineItemSchema(sku='SKU-1', quantity=1, unit_price=10.0)],
            total_amount=10.0,
            currency='USD',
        )

        result = await service.submit_order(request=request, res_obj=response)

        assert result.order_id == 'order-1'
        assert result.status == 'Заказ получен'
        assert result.request_id

        apply_connection_settings_mock.assert_awaited_once_with(
            response_delay=2,
            response_code=202,
            res_obj=response,
            db_session=session,
        )
        processor_request_dao.add_request.assert_awaited_once()
        inserted_values = processor_request_dao.add_request.await_args.kwargs['values']
        assert inserted_values.order_id == 'order-1'
        assert inserted_values.customer_id == 'customer-1'

    async def test_submit_order_raises_immediate_422_when_post_mode_has_error(self, mocker):
        processor_request_dao = mocker.Mock()
        processor_request_dao.add_request = mocker.AsyncMock()

        post_error = {
            'validationError': {
                'detail': [
                    {
                        'loc': ['body', 'order_id'],
                        'msg': 'emulated',
                        'type': 'value_error.mock',
                    }
                ]
            }
        }
        processor_settings_dao = mocker.Mock()
        processor_settings_dao.get_endpoint_full_config = mocker.AsyncMock(
            return_value=self._build_full_config(post_error=post_error),
        )

        apply_connection_settings_mock = mocker.patch(
            'app.api.processor.services.processor_service.ConnectionEmulationService.apply_connection_settings',
            new=mocker.AsyncMock(),
        )

        service = ProcessorService(
            processor_request_dao=processor_request_dao,
            processor_settings_dao=processor_settings_dao,
            session=mocker.Mock(),
        )
        response = Response()
        request = ProcessorSubmitRequestSchema(
            order_id='order-1',
            customer_id='customer-1',
            items=[OrderLineItemSchema(sku='SKU-1', quantity=1, unit_price=10.0)],
            total_amount=10.0,
            currency='USD',
        )

        with pytest.raises(ProcessorSubmitError):
            await service.submit_order(request=request, res_obj=response)

        apply_connection_settings_mock.assert_awaited_once()
        processor_request_dao.add_request.assert_not_awaited()

    async def test_get_order_status_applies_settings_and_returns_status(self, mocker):
        processor_request_dao = mocker.Mock()
        processor_request_dao.find_request_and_status = mocker.AsyncMock(
            return_value={
                'request': {
                    'request_id': 'req-1',
                    'endpoint_type': 'submit',
                    'order_id': 'order-1',
                    'customer_id': 'customer-1',
                    'response_delay': 1,
                    'response_code': 200,
                    'post_mode_id': 1,
                    'status_mode_id': 1,
                    'status_step_id': 2,
                    'status_change_after': None,
                    'unixtimestamp': 1710000000,
                    'payload': {'order_id': 'order-1'},
                },
                'status_mode_steps': {
                    'id': 2,
                    'status_mode_id': 1,
                    'step_order': 2,
                    'status': 'Упаковка',
                    'duration': 5,
                    'error_message': None,
                },
            }
        )

        processor_settings_dao = mocker.Mock()
        processor_settings_dao.get_endpoint_settings = mocker.AsyncMock(
            return_value=SimpleNamespace(response_delay=3, response_code=201),
        )

        apply_connection_settings_mock = mocker.patch(
            'app.api.processor.services.processor_service.ConnectionEmulationService.apply_connection_settings',
            new=mocker.AsyncMock(),
        )

        session = mocker.Mock()
        service = ProcessorService(
            processor_request_dao=processor_request_dao,
            processor_settings_dao=processor_settings_dao,
            session=session,
        )
        response = Response()

        result = await service.get_order_status(request_id='req-1', res_obj=response)

        assert result.request_id == 'req-1'
        assert result.order_id == 'order-1'
        assert result.status == 'Упаковка'

        apply_connection_settings_mock.assert_awaited_once_with(
            response_delay=3,
            response_code=201,
            res_obj=response,
            db_session=session,
        )
        processor_request_dao.find_request_and_status.assert_awaited_once_with(
            session=session,
            request_id='req-1',
        )

    async def test_get_order_status_raises_404_when_request_is_missing(self, mocker):
        processor_request_dao = mocker.Mock()
        processor_request_dao.find_request_and_status = mocker.AsyncMock(return_value=None)

        processor_settings_dao = mocker.Mock()
        processor_settings_dao.get_endpoint_settings = mocker.AsyncMock(
            return_value=SimpleNamespace(response_delay=0, response_code=200),
        )
        mocker.patch(
            'app.api.processor.services.processor_service.ConnectionEmulationService.apply_connection_settings',
            new=mocker.AsyncMock(),
        )

        service = ProcessorService(
            processor_request_dao=processor_request_dao,
            processor_settings_dao=processor_settings_dao,
            session=mocker.Mock(),
        )

        with pytest.raises(HTTPException, match='request_id'):
            await service.get_order_status(request_id='missing', res_obj=Response())

    async def test_get_requests_returns_records_from_dao(self, mocker):
        session = mocker.Mock()
        processor_request_dao = mocker.Mock()
        processor_request_dao.find_requests = mocker.AsyncMock(
            return_value=[
                SimpleNamespace(
                    id=1,
                    request_id='req-1',
                    endpoint_type='submit',
                    order_id='order-1',
                    customer_id='customer-1',
                    response_delay=2,
                    response_code=202,
                    post_mode_id=1,
                    status_mode_id=1,
                    status_step_id=11,
                    status_change_after=None,
                    unixtimestamp=1710000000,
                    payload={'order_id': 'order-1'},
                    created='2026-04-19T10:00:00Z',
                    updated='2026-04-19T10:00:00Z',
                )
            ]
        )
        processor_settings_dao = mocker.Mock()

        service = ProcessorService(
            processor_request_dao=processor_request_dao,
            processor_settings_dao=processor_settings_dao,
            session=session,
        )

        result = await service.get_requests()

        assert len(result) == 1
        assert result[0].request_id == 'req-1'
        assert result[0].order_id == 'order-1'
        processor_request_dao.find_requests.assert_awaited_once_with(session=session)

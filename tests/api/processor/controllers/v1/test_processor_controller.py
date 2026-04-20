import pytest

from fastapi import Response

from app.api.processor.controllers.v1 import processor_controller


@pytest.mark.asyncio
class TestProcessorController:
    async def test_submit_order_returns_service_response(self, order_submit_request, order_submit_response, mocker):
        service = mocker.Mock()
        service.submit_order = mocker.AsyncMock(return_value=order_submit_response)
        response_obj = Response()

        result = await processor_controller.submit_order(
            request=order_submit_request,
            response=response_obj,
            service=service,
        )

        assert result == order_submit_response
        service.submit_order.assert_awaited_once_with(request=order_submit_request, res_obj=response_obj)

    async def test_get_order_status_returns_service_response(self, order_status_response, mocker):
        service = mocker.Mock()
        service.get_order_status = mocker.AsyncMock(return_value=order_status_response)
        response_obj = Response()

        result = await processor_controller.get_order_status(
            request_id='req-1',
            response=response_obj,
            service=service,
        )

        assert result == order_status_response
        service.get_order_status.assert_awaited_once_with(request_id='req-1', res_obj=response_obj)

    async def test_get_order_status_reraises_service_error(self, mocker):
        service = mocker.Mock()
        service.get_order_status = mocker.AsyncMock(side_effect=RuntimeError('сервис завершился с ошибкой'))
        response_obj = Response()

        with pytest.raises(RuntimeError, match='сервис завершился с ошибкой'):
            await processor_controller.get_order_status(
                request_id='req-1',
                response=response_obj,
                service=service,
            )

    async def test_get_requests_returns_service_response(self, order_request_response, mocker):
        service = mocker.Mock()
        service.get_requests = mocker.AsyncMock(return_value=[order_request_response])

        result = await processor_controller.get_requests(service=service)

        assert result == [order_request_response]
        service.get_requests.assert_awaited_once_with()

    async def test_get_requests_reraises_service_error(self, mocker):
        service = mocker.Mock()
        service.get_requests = mocker.AsyncMock(side_effect=RuntimeError('сервис завершился с ошибкой'))

        with pytest.raises(RuntimeError, match='сервис завершился с ошибкой'):
            await processor_controller.get_requests(service=service)

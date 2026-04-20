import asyncio

from starlette.requests import Request
from starlette.responses import Response

from app.api.fastapi_middlewares.logging_middleware import log_request_reponse


class TestLoggingMiddleware:
    def test_log_request_with_body(self, mocker):
        payload = {'data': 123}
        metadata = {
            'type': 'http',
            'method': 'POST',
            'url': '/processor/api/v1/order',
            'headers': [],
            'path': '',
        }

        request = Request(metadata)

        # Мокаем req.json()
        request.json = mocker.AsyncMock(return_value=payload)

        # Мокаем call_next
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 200
        call_next = mocker.AsyncMock(return_value=mock_response)

        # Вызов fastapi_middlewares
        result = asyncio.run(log_request_reponse(request=request, call_next=call_next))

        # Проверка
        assert result.status_code == 200
        assert request.state.req_body == payload
        call_next.assert_called_once_with(request)

    def test_log_request_without_body(self, mocker):
        metadata = {
            'type': 'http',
            'method': 'GET',
            'url': '/processor/api/v1/status',
            'headers': [],
            'path': '',
        }

        request = Request(metadata)

        # Мокаем req.json()
        request.json = mocker.AsyncMock(side_effect=ValueError('Нет JSON-тела'))

        # Мокаем call_next
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 200
        call_next = mocker.AsyncMock(return_value=mock_response)

        # Вызов fastapi_middlewares
        result = asyncio.run(log_request_reponse(request=request, call_next=call_next))

        # Проверка
        assert result.status_code == 200
        assert not hasattr(request.state, 'req_body')
        call_next.assert_called_once_with(request)

    def test_skip_logging_for_metrics_path(self, mocker):
        payload = {'data': 123}
        metadata = {
            'type': 'http',
            'method': 'POST',
            'url': '/metrics',
            'headers': [],
            'path': '/metrics',
        }

        request = Request(metadata)
        request.json = mocker.AsyncMock(return_value=payload)

        mock_response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 200
        call_next = mocker.AsyncMock(return_value=mock_response)
        logger_info = mocker.patch('app.api.fastapi_middlewares.logging_middleware.logger.info')

        result = asyncio.run(log_request_reponse(request=request, call_next=call_next))

        assert result.status_code == 200
        assert not hasattr(request.state, 'req_body')
        request.json.assert_not_awaited()
        logger_info.assert_not_called()
        call_next.assert_called_once_with(request)

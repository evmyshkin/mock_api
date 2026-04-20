import time

from collections.abc import Callable

from fastapi import Request
from fastapi import Response
from loguru import logger

from app.config import config

METHODS_WITHOUT_BODY = {'GET', 'HEAD', 'OPTIONS'}
EXTRA_API_PATH_PREFIXES = ('/healthcheck', '/metrics')


def _is_extra_api_path(path: str) -> bool:
    """Проверить, относится ли путь к extra_api ручкам."""
    return any(path == prefix or path.startswith(f'{prefix}/') for prefix in EXTRA_API_PATH_PREFIXES)


def _truncate_body(body: object) -> str:
    """Обрезать тело запроса для безопасного логирования."""
    body_str = str(body)
    max_chars = config.common.request_body_log_max_chars
    if len(body_str) <= max_chars:
        return body_str

    overflow = len(body_str) - max_chars
    return f'{body_str[:max_chars]}...<truncated {overflow} chars>'


async def log_request_reponse(request: Request, call_next: Callable) -> Response:
    """Миддлвер для логирования запросов и ответов."""
    if _is_extra_api_path(request.url.path):
        return await call_next(request)

    start_time = time.perf_counter()
    req_method = request.method
    req_url = request.url

    msg = f'Поступил запрос {req_method=}, {req_url=}'
    try:
        if req_method not in METHODS_WITHOUT_BODY:
            # Добавляем в атрибут state, чтобы не потреблять тело повторно downstream.
            request.state.req_body = await request.json()
            msg += f', req_body={_truncate_body(request.state.req_body)}'
    except ValueError as e:
        logger.debug('У запроса нет тела. Не логируем тело.', e)

    # Вызов ответа
    res: Response = await call_next(request)
    res_status = res.status_code
    res_process_time = time.perf_counter() - start_time

    # Логируем ответ
    msg += f', {res_status=}, {res_process_time=:.3f}'
    logger.info(msg)

    return res

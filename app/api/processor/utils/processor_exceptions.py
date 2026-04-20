from typing import Any


class ProcessorSubmitError(Exception):
    """Пользовательская ошибка для эмулированных сбоев отправки."""

    def __init__(self, status_code: int, msg: Any) -> None:
        self.msg = msg
        self.status_code = status_code

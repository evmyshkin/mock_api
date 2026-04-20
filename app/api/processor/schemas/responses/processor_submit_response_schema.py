from typing import Annotated

from pydantic import Field

from app.api.common.schemas.base_schema import BaseSchema


class ProcessorSubmitResponseSchema(BaseSchema):
    """Контракт ответа для эндпоинтов отправки заказа и получения статуса."""

    request_id: Annotated[str, Field(description='Уникальный идентификатор запроса для опроса статуса.')]
    order_id: Annotated[str, Field(description='Идентификатор заказа из тела отправки.')]
    status: Annotated[str, Field(description='Текущий статус обработки заказа.')]
    unixtimestamp: Annotated[int, Field(description='Unix-время регистрации запроса.')]
    error_message: Annotated[list[dict] | None, Field(description='Опциональное тело ошибки статуса.')] = None

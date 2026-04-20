from datetime import datetime
from typing import Annotated
from typing import Any

from pydantic import Field

from app.api.common.schemas.base_schema import BaseSchema


class ProcessorRequestResponseSchema(BaseSchema):
    """Схема сохраненной записи запроса обработки заказа."""

    id: Annotated[int, Field(description='Идентификатор записи.', ge=1)]
    request_id: Annotated[str, Field(description='Уникальный идентификатор запроса.')]
    endpoint_type: Annotated[str, Field(description='Тип endpoint, где была создана запись.')]
    order_id: Annotated[str, Field(description='Идентификатор заказа.')]
    customer_id: Annotated[str, Field(description='Идентификатор клиента.')]
    response_delay: Annotated[int, Field(description='Задержка ответа в секундах.')]
    response_code: Annotated[int, Field(description='HTTP-код ответа.')]
    post_mode_id: Annotated[int, Field(description='Идентификатор post mode.')]
    status_mode_id: Annotated[int, Field(description='Идентификатор status mode.')]
    status_step_id: Annotated[int, Field(description='Идентификатор текущего шага статуса.')]
    status_change_after: Annotated[datetime | None, Field(description='Время планового перехода статуса.')]
    unixtimestamp: Annotated[int, Field(description='Unix-время регистрации запроса.')]
    payload: Annotated[dict[str, Any] | list[Any], Field(description='Сохраненное тело исходного запроса.')]
    created: Annotated[datetime, Field(description='Время создания записи.')]
    updated: Annotated[datetime, Field(description='Время обновления записи.')]

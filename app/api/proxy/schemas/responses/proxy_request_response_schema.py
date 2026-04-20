from datetime import datetime
from typing import Annotated
from typing import Any

from pydantic import Field

from app.api.common.schemas.base_schema import BaseSchema


class ProxyRequestResponseSchema(BaseSchema):
    """Данные сохраненного запроса загрузки товара."""

    request_id: Annotated[str, Field(description='Уникальный идентификатор запроса для обновления или вставки записи.')]
    query_params: Annotated[dict[str, Any], Field(description='Параметры запроса, сохраненные из входящего запроса.')]
    headers: Annotated[dict[str, Any], Field(description='Заголовки, сохраненные из входящего запроса.')]
    body: Annotated[dict[str, Any], Field(description='Сохраненное тело запроса в формате JSON.')]
    created: Annotated[datetime, Field(description='Время создания записи.')]
    updated: Annotated[datetime, Field(description='Время обновления записи.')]

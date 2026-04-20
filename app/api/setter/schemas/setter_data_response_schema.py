from datetime import datetime
from typing import Annotated
from typing import Any

from pydantic import Field

from app.api.common.schemas.base_schema import BaseSchema


class SetterDataResponseSchema(BaseSchema):
    """Схема отладочного ответа для сохраненных записей витрины."""

    id: Annotated[int, Field(description='Идентификатор записи.', ge=1)]
    entity_type: Annotated[str, Field(description='Тип сущности витрины.')]
    payload: Annotated[dict[str, Any], Field(description='Сохраненное тело данных.')]
    is_validated: Annotated[bool, Field(description='Признак, что данные записаны через строгий эндпоинт записи.')]
    created: Annotated[datetime, Field(description='Время создания записи.')]
    updated: Annotated[datetime, Field(description='Время обновления записи.')]

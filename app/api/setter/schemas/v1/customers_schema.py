from datetime import datetime
from typing import Annotated
from typing import Any

from pydantic import Field

from app.api.common.schemas.base_root_schema import BaseRootSchema
from app.api.common.schemas.base_schema import BaseSchema


class CustomerItemSchema(BaseSchema):
    """Схема элемента данных клиента для строгой валидации."""

    customer_id: Annotated[str, Field(description='Идентификатор клиента.', min_length=1)]
    email: Annotated[str, Field(description='Email клиента.', min_length=3)]
    first_name: Annotated[str, Field(description='Имя клиента.', min_length=1)]
    last_name: Annotated[str, Field(description='Фамилия клиента.', min_length=1)]
    is_active: Annotated[bool, Field(description='Признак активности клиента.')]
    registered_at: Annotated[datetime, Field(description='Временная метка регистрации.')]


class CustomersSetRequestSchema(BaseRootSchema):
    """Строгое тело запроса для эндпоинта записи клиентов."""

    root: Annotated[list[CustomerItemSchema], Field(min_length=1)]


class CustomersSetOpenRequestSchema(BaseRootSchema):
    """Тело запроса свободного формата для эндпоинта записи клиентов (произвольные объекты)."""

    root: Annotated[list[dict[str, Any]], Field(min_length=1)]


class CustomersGetResponseSchema(BaseSchema):
    """Схема ответа эндпоинта чтения клиентов."""

    items: Annotated[list[dict[str, Any]], Field(description='Накопленные данные клиентов.')]

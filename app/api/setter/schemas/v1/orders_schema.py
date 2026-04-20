from datetime import datetime
from typing import Annotated
from typing import Any

from pydantic import Field

from app.api.common.schemas.base_root_schema import BaseRootSchema
from app.api.common.schemas.base_schema import BaseSchema


class OrderItemSchema(BaseSchema):
    """Схема элемента данных заказа для строгой валидации."""

    order_id: Annotated[str, Field(description='Идентификатор заказа.', min_length=1)]
    customer_id: Annotated[str, Field(description='Идентификатор клиента.', min_length=1)]
    product_ids: Annotated[list[str], Field(description='Идентификаторы заказанных товаров.', min_length=1)]
    total_amount: Annotated[float, Field(description='Общая сумма заказа.', ge=0)]
    currency: Annotated[
        str,
        Field(description='Код валюты по ISO.', min_length=3, max_length=3, pattern='^[A-Z]{3}$'),
    ]
    status: Annotated[str, Field(description='Статус заказа.', min_length=1)]
    created_at: Annotated[datetime, Field(description='Временная метка создания.')]


class OrdersSetRequestSchema(BaseRootSchema):
    """Строгое тело запроса для эндпоинта записи заказов."""

    root: Annotated[list[OrderItemSchema], Field(min_length=1)]


class OrdersSetOpenRequestSchema(BaseRootSchema):
    """Тело запроса свободного формата для эндпоинта записи заказов (произвольные объекты)."""

    root: Annotated[list[dict[str, Any]], Field(min_length=1)]


class OrdersGetResponseSchema(BaseSchema):
    """Схема ответа эндпоинта чтения заказов."""

    items: Annotated[list[dict[str, Any]], Field(description='Накопленные данные заказов.')]

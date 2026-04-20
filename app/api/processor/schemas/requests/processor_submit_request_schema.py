from typing import Annotated

from pydantic import ConfigDict
from pydantic import Field

from app.api.common.schemas.base_schema import BaseSchema


class OrderLineItemSchema(BaseSchema):
    """Позиция в теле отправки заказа."""

    model_config = ConfigDict(extra='forbid')

    sku: Annotated[str, Field(description='Идентификатор SKU.', min_length=1)]
    quantity: Annotated[int, Field(description='Заказанное количество.', ge=1)]
    unit_price: Annotated[float, Field(description='Цена за единицу SKU.', ge=0)]


class ProcessorSubmitRequestSchema(BaseSchema):
    """Строгая схема запроса для эндпоинта отправки заказа в обработку."""

    model_config = ConfigDict(extra='forbid')

    order_id: Annotated[str, Field(description='Идентификатор заказа.', min_length=1)]
    customer_id: Annotated[str, Field(description='Идентификатор клиента.', min_length=1)]
    items: Annotated[list[OrderLineItemSchema], Field(description='Позиции заказа.', min_length=1)]
    total_amount: Annotated[float, Field(description='Общая сумма заказа.', ge=0)]
    currency: Annotated[
        str,
        Field(description='Код валюты по ISO.', min_length=3, max_length=3, pattern='^[A-Z]{3}$'),
    ]
